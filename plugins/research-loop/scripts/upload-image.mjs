#!/usr/bin/env node
// Pass the prepare result JSON through stdin, never a signed URL as an argument.
import { readFile, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

class UploadError extends Error {}

export function validateTicket(payload) {
  const ticket = payload?.structuredContent?.data ?? payload?.data ?? payload;
  if (ticket?.status !== 'awaiting_upload' || ticket.method !== 'PUT'
    || !/^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$/.test(ticket.projectId ?? '')
    || !/^[A-Za-z0-9][A-Za-z0-9._:-]{0,159}$/.test(ticket.objectId ?? '')
    || !Number.isInteger(ticket.size) || ticket.size < 1 || ticket.size > 10 * 1024 * 1024
    || !/^[0-9a-f]{64}$/.test(ticket.sha256 ?? '')) throw new UploadError('Invalid upload ticket.');
  const url = new URL(ticket.uploadUrl);
  const prefix = `/storage/v1/object/upload/sign/research-media/${ticket.projectId}/${ticket.objectId}/`;
  const path = decodeURIComponent(url.pathname);
  if (url.protocol !== 'https:' || url.hostname !== 'ezmkpdnchcpjuvpilpxu.supabase.co'
    || url.port || url.username || url.password || url.hash
    || !path.startsWith(prefix) || !/^[0-9a-f-]{36}\.(png|jpg|webp|gif)$/.test(path.slice(prefix.length))
    || !url.searchParams.get('token') || [...url.searchParams.keys()].some((key)=>key !== 'token')) {
    throw new UploadError('Upload destination is not the reserved Research Loop image path.');
  }
  const mime = ticket.headers?.['Content-Type'];
  if (!['image/png','image/jpeg','image/webp','image/gif'].includes(mime)) throw new UploadError('Unsupported image type.');
  return { ticket, url: url.toString(), mime };
}

async function main() {
  const filePath = process.argv[2];
  if (!filePath || process.argv.length !== 3) throw new UploadError('Usage: node upload-image.mjs /path/to/figure.png (prepare result JSON on stdin)');
  const chunks = []; let total = 0;
  for await (const chunk of process.stdin) {
    total += chunk.length;
    if (total > 65536) throw new UploadError('Upload ticket is too large.');
    chunks.push(chunk);
  }
  const { ticket, url, mime } = validateTicket(JSON.parse(Buffer.concat(chunks).toString('utf8')));
  const info = await stat(filePath);
  if (!info.isFile() || info.size !== ticket.size) throw new UploadError('File size does not match the prepared image.');
  const file = await readFile(filePath);
  if (file.length !== ticket.size || createHash('sha256').update(file).digest('hex') !== ticket.sha256) {
    throw new UploadError('File changed after preparation. Prepare a new upload for the current file.');
  }
  let response;
  try {
    response = await fetch(url,{method:'PUT',headers:{'Content-Type':mime},body:file,
      redirect:'error',signal:AbortSignal.timeout(120000)});
  } catch { throw new UploadError('Upload result is uncertain. Call complete_research_media_upload before retrying this ticket.'); }
  if (!response.ok) throw new UploadError(`Upload returned HTTP ${response.status}. Call complete_research_media_upload to check uncertain or duplicate delivery; no file was overwritten.`);
  process.stdout.write(JSON.stringify({uploaded:true,attached:false,upload_id:ticket.uploadId,
    nextStep:'Call complete_research_media_upload, then save_research_page with its persistent media reference.'})+'\n');
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error)=>{
    // Known application messages only. Never include raw network errors or URLs.
    const message = error instanceof UploadError
      ? error.message : 'Image upload failed. Check the ticket and retry completion.';
    process.stderr.write(message+'\n'); process.exitCode=1;
  });
}
