// eslint-disable-next-line @typescript-eslint/no-var-requires
const plugin = require('tailwindcss/plugin')

const toPX = values => Object.fromEntries(values.map(v => [+v, `${v}px`]))
const object0to100px = toPX(Array.from({ length: 101 }).map((_, i) => +i))

const fallbackSansSerifFonts = [
  '-apple-system',
  'BlinkMacSystemFont',
  'Segoe UI',
  'Helvetica',
  'Arial',
  'sans-serif'
]

module.exports = {
  plugins: [
    require('@tailwindcss/aspect-ratio'),

    plugin(({ addUtilities }) => {
      const typographyWithOnlySizes = {}
      for (let i = 8; i <= 100; i += 2) {
        typographyWithOnlySizes[`.text-${i}`] = { fontSize: `${i}px` }
      }

      addUtilities(typographyWithOnlySizes)
    })
  ],

  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],

  corePlugins: {
    aspectRatio: false,
    container: false
  },

  theme: {
    extend: {
      borderColor: {
        DEFAULT: 'transparent'
      },

      scale: {
        101: '1.01'
      }
    },

    screens: {
      xl: { max: '1529.99px' },
      lg: { max: '1199.99px' },
      md: { max: '991.99px' },
      sm: { max: '767.99px' },
      xs: { max: '575.99px' },
    },

    fontSize: false,

    spacing: object0to100px,

    borderWidth: {
      DEFAULT: '1px',
      ...object0to100px
    },

    borderRadius: {
      ...object0to100px,
      full: '9999px'
    },

    fontFamily: {
      sans: ['Montserrat', ...fallbackSansSerifFonts],
    }
  }
}
