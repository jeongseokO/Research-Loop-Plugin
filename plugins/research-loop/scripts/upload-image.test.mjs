import test from 'node:test';
import assert from 'node:assert/strict';
import { validateTicket } from './upload-image.mjs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ticket = {status:'awaiting_upload',method:'PUT',projectId:'p',objectId:'o',size:68,sha256:'a'.repeat(64),
  headers:{'Content-Type':'image/png'},
  uploadUrl:'https://ezmkpdnchcpjuvpilpxu.supabase.co/storage/v1/object/upload/sign/research-media/p/o/123e4567-e89b-42d3-a456-426614174000.png?token=example-only'};
test('accepts direct and structured MCP tickets',()=>{
  assert.equal(validateTicket(ticket).mime,'image/png');
  assert.equal(validateTicket({structuredContent:{data:ticket}}).ticket.projectId,'p');
});
test('rejects foreign hosts, object paths, redirects and unsupported types',()=>{
  for (const uploadUrl of [ticket.uploadUrl.replace('ezmkpdnchcpjuvpilpxu.supabase.co','evil.test'),
    ticket.uploadUrl.replace('/p/o/','/other/o/'),ticket.uploadUrl.replace('https:','http:'),
    ticket.uploadUrl+'&redirect=https://evil.test',ticket.uploadUrl.replace('.png?','.html?')]) {
    assert.throws(()=>validateTicket({...ticket,uploadUrl}));
  }
  assert.throws(()=>validateTicket({...ticket,headers:{'Content-Type':'image/svg+xml'}}));
  assert.throws(()=>validateTicket({...ticket,size:11*1024*1024}));
});
test('CLI errors never reveal raw ticket contents or local file paths',()=>{
  for (const input of ['{"BAD_SECRET": not-json}',JSON.stringify(ticket)]) {
    const result=spawnSync(process.execPath,[fileURLToPath(new URL('./upload-image.mjs',import.meta.url)),
      '/synthetic/private-research-name/figure.png'],{input,encoding:'utf8'});
    assert.equal(result.status,1);
    assert.equal(result.stderr.includes('BAD_SECRET'),false);
    assert.equal(result.stderr.includes('private-research-name'),false);
    assert.equal(result.stderr.includes('example-only'),false);
    assert.equal(result.stdout,'');
  }
});
