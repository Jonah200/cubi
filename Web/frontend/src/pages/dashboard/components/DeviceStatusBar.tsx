import { useRef, useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import Modal from '@/components/Modal'
import { useAssociateDevice } from '@/hooks/queries'

const CODE_LENGTH = 6

export default function DeviceStatusBar() {
  const [open, setOpen] = useState(false)
  const [code, setCode] = useState(Array(CODE_LENGTH).fill(''))
  const [error, setError] = useState<string | null>(null)
  const [connected, setConnected] = useState(false)
  const inputsRef = useRef<(HTMLInputElement | null)[]>([])
  const associate = useAssociateDevice()

  function resetState() {
    setCode(Array(CODE_LENGTH).fill(''))
    setError(null)
    associate.reset()
  }

  function handleOpen() {
    resetState()
    setOpen(true)
  }

  function handleChange(index: number, value: string) {
    if (!/^[a-zA-Z0-9]?$/.test(value)) return
    const next = [...code]
    next[index] = value.toUpperCase()
    setCode(next)
    setError(null)

    if (value && index < CODE_LENGTH - 1) {
      inputsRef.current[index + 1]?.focus()
    }
  }

  function handleKeyDown(index: number, e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      inputsRef.current[index - 1]?.focus()
    }
  }

  function handlePaste(e: React.ClipboardEvent) {
    e.preventDefault()
    const pasted = e.clipboardData.getData('text').replace(/[^a-zA-Z0-9]/g, '').toUpperCase().slice(0, CODE_LENGTH)
    if (!pasted) return
    const next = [...code]
    for (let i = 0; i < pasted.length; i++) {
      next[i] = pasted[i]
    }
    setCode(next)
    const focusIndex = Math.min(pasted.length, CODE_LENGTH - 1)
    inputsRef.current[focusIndex]?.focus()
  }

  function handleSubmit() {
    const fullCode = code.join('')
    if (fullCode.length < CODE_LENGTH) {
      setError('Please enter the full 6-character code.')
      return
    }

    associate.mutate(fullCode, {
      onSuccess: () => {
        setConnected(true)
        setOpen(false)
      },
      onError: () => {
        setError('Invalid code. Check your device and try again.')
      },
    })
  }

  if (connected) {
    return (
      <div className="flex items-center gap-3">
        <Badge variant="outline" className="gap-1.5">
          <span className="inline-block h-2 w-2 rounded-full bg-green-500" />
          Device connected
        </Badge>
      </div>
    )
  }

  return (
    <>
      <div className="flex items-center gap-3">
        <Badge variant="outline" className="gap-1.5">
          <span className="inline-block h-2 w-2 rounded-full bg-red-500" />
          No device connected
        </Badge>
        <Button variant="link" className="h-auto p-0 text-sm" onClick={handleOpen}>
          Connect now
        </Button>
      </div>

      <Modal
        open={open}
        onOpenChange={setOpen}
        title="Connect Device"
        description="Enter the 6-character code shown on your LAMPI device."
      >
        <div className="flex flex-col items-center gap-6 pt-2">
          <div className="flex gap-2" onPaste={handlePaste}>
            {code.map((digit, i) => (
              <input
                key={i}
                ref={(el) => { inputsRef.current[i] = el }}
                type="text"
                inputMode="text"
                maxLength={1}
                value={digit}
                onChange={(e) => handleChange(i, e.target.value)}
                onKeyDown={(e) => handleKeyDown(i, e)}
                className="h-12 w-10 rounded-md border border-input bg-background text-center font-mono text-lg uppercase focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
            ))}
          </div>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <Button
            className="w-full"
            onClick={handleSubmit}
            disabled={associate.isPending}
          >
            {associate.isPending ? 'Connecting...' : 'Connect'}
          </Button>
        </div>
      </Modal>
    </>
  )
}
