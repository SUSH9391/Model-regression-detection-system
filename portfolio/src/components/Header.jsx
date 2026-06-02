import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const NAV_ITEMS = [
  { label: 'HOME',     path: '/' },
  { label: 'RESUME',   path: '/resume' },
  { label: 'PROJECTS', path: '/projects' },
  { label: 'CONTACT',  path: '/contact' },
]

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false)
  const navigate = useNavigate()

  // Prevent body scroll when nav is open
  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [menuOpen])

  const handleNavClick = (path) => {
    setMenuOpen(false)
    navigate(path)
  }

  return (
    <>
      {/* Full-screen nav overlay */}
      <nav className={`openNavDesk${menuOpen ? ' showNavDesktop' : ''}`}>
        <span
          className="navCloseBtn"
          onClick={() => setMenuOpen(false)}
          aria-label="Close navigation"
        >
          ✕
        </span>
        <ul className="navList">
          {NAV_ITEMS.map((item) => (
            <li key={item.label}>
              <a
                href={item.path}
                onClick={(e) => { e.preventDefault(); handleNavClick(item.path) }}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>

      {/* Sticky header bar */}
      <header className="headerComp">
        <div className="headerInner">
          {/* Hamburger */}
          <div
            className={`main-item menu${menuOpen ? ' close' : ''}`}
            onClick={() => setMenuOpen((o) => !o)}
            aria-label="Toggle navigation"
            role="button"
          >
            <span className="line line01" />
            <span className="line line02" />
            <span className="line line03" />
          </div>

          {/* Logo */}
          <Link to="/" className="logoLink" onClick={() => setMenuOpen(false)}>
            <h1 className="logoTitle">Shad</h1>
          </Link>

          {/* Connect button */}
          <a
            href="https://www.linkedin.com/in/shadmansohel/"
            target="_blank"
            rel="noopener noreferrer"
            className="pillBtn connectBtn"
          >
            Connect
          </a>
        </div>
      </header>
    </>
  )
}
