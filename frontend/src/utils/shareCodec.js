import LZString from 'lz-string'

const SHARE_VERSION = 'v1'
const { compressToUint8Array, decompressFromUint8Array } = LZString

function bytesToBase64Url(bytes) {
  let binary = ''
  const chunkSize = 0x8000

  for (let index = 0; index < bytes.length; index += chunkSize) {
    binary += String.fromCharCode(...bytes.subarray(index, index + chunkSize))
  }

  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '')
}

function base64UrlToBytes(base64Url) {
  const paddingLength = (4 - (base64Url.length % 4)) % 4
  const base64 = `${base64Url.replace(/-/g, '+').replace(/_/g, '/')}${'='.repeat(paddingLength)}`
  const binary = atob(base64)
  const bytes = new Uint8Array(binary.length)

  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index)
  }

  return bytes
}

function decodeV1(payload) {
  const compressed = base64UrlToBytes(payload)
  const json = decompressFromUint8Array(compressed)

  if (json === null) {
    throw new Error('Invalid shared code payload')
  }

  const parsed = JSON.parse(json)

  if (typeof parsed !== 'string') {
    throw new Error('Invalid shared code format')
  }

  return parsed
}

export function encodeSharedCode(code) {
  const json = JSON.stringify(code)
  const compressed = compressToUint8Array(json)
  const payload = bytesToBase64Url(compressed)

  return `${SHARE_VERSION}:${payload}`
}

export function decodeSharedCode(fragment) {
  const normalized = fragment.startsWith('#') ? fragment.slice(1) : fragment
  const separatorIndex = normalized.indexOf(':')

  if (separatorIndex === -1) {
    throw new Error('Missing shared code version')
  }

  const version = normalized.slice(0, separatorIndex)
  const payload = normalized.slice(separatorIndex + 1)

  if (!payload) {
    throw new Error('Missing shared code payload')
  }

  switch (version) {
    case SHARE_VERSION:
      return decodeV1(payload)
    default:
      throw new Error(`Unsupported shared code version: ${version}`)
  }
}
