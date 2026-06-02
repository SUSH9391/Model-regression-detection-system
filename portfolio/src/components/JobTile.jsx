import { useState, useEffect, useRef } from 'react'

export default function JobTile({ title, company, date, description, shift = 'none' }) {
  const [open, setOpen] = useState(false)
  const [visible, setVisible] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); observer.disconnect() } },
      { threshold: 0.15 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  const shiftClass = shift === 'right' ? 'rightShift' : shift === 'left' ? 'leftShift' : ''

  return (
    <div
      ref={ref}
      className={`jobTile ${shiftClass} ${visible ? 'animateJob' : ''} ${open ? 'openHeight' : ''}`}
      onClick={() => setOpen((o) => !o)}
      role="button"
      aria-expanded={open}
    >
      <div className="topRes">
        <h1>{title}</h1>
        <span>{date}</span>
      </div>
      <h2>{company}</h2>
      <p>{description}</p>
    </div>
  )
}
