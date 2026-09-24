const { existsSync } = require('node:fs')
const path = require('node:path')
const { spawn } = require('node:child_process')

const projectRoot = path.resolve(__dirname, '..')
const backendDir = path.join(projectRoot, 'backend')
const isWindows = process.platform === 'win32'

const venvPython = isWindows
  ? path.join(projectRoot, '.venv', 'Scripts', 'python.exe')
  : path.join(projectRoot, '.venv', 'bin', 'python')

const candidates = [
  venvPython,
  process.env.PYTHON,
  isWindows ? 'python' : 'python3',
].filter(Boolean)

const python = candidates.find((candidate) => (
  candidate === 'python' || candidate === 'python3' || existsSync(candidate)
))

if (!python) {
  const venvPythonCommand = isWindows ? '.venv\\Scripts\\python.exe' : '.venv/bin/python'
  console.error(
    'Could not find Python. Create a virtual environment with:\n' +
    '  python -m venv .venv\n' +
    `  ${venvPythonCommand} -m pip install -r backend/requirements.txt`,
  )
  process.exit(1)
}

const args = [
  '-m', 'uvicorn',
  'main:app',
  '--reload',
  '--host', process.env.API_HOST || '127.0.0.1',
  '--port', process.env.API_PORT || '8000',
]

const child = spawn(python, args, {
  cwd: backendDir,
  stdio: 'inherit',
  windowsHide: false,
})

child.on('error', (error) => {
  console.error(`Failed to start FastAPI: ${error.message}`)
  process.exit(1)
})

child.on('exit', (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal)
  } else {
    process.exit(code ?? 1)
  }
})

for (const signal of ['SIGINT', 'SIGTERM']) {
  process.on(signal, () => {
    if (!child.killed) child.kill(signal)
  })
}
