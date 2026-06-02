import { useState } from 'react'

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', message: '' })
  const [sent, setSent] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: wire up to your preferred email service (EmailJS, Formspree, etc.)
    console.log('Form submitted:', form)
    setSent(true)
    setForm({ name: '', email: '', message: '' })
    setTimeout(() => setSent(false), 4000)
  }

  return (
    <div className="contactPage">
      <h1>CONTACT</h1>

      <div className="contactForm">
        {/* Left — headline */}
        <div className="leftContact">
          <h2>LET'S<br />TALK.</h2>
        </div>

        {/* Right — form */}
        <form className="rightForm" onSubmit={handleSubmit} noValidate>
          <div className="formGroup">
            <h3>Your Name</h3>
            <input
              id="contact-name"
              type="text"
              name="name"
              placeholder="John Doe"
              value={form.name}
              onChange={handleChange}
              required
              autoComplete="name"
            />
          </div>

          <div className="formGroup">
            <h3>Email Address</h3>
            <input
              id="contact-email"
              type="email"
              name="email"
              placeholder="john@example.com"
              value={form.email}
              onChange={handleChange}
              required
              autoComplete="email"
            />
          </div>

          <div className="formGroup">
            <h3>Message</h3>
            <textarea
              id="contact-message"
              name="message"
              placeholder="What's on your mind?"
              value={form.message}
              onChange={handleChange}
              required
            />
          </div>

          <button id="contact-submit" type="submit" className="submitBtn">
            {sent ? 'Message Sent ✓' : 'Send Message'}
          </button>
        </form>
      </div>
    </div>
  )
}
