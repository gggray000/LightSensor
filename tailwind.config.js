/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      fontFamily: {
                'RiftRegular': ['Rift-Regular'],
                'RiftMedium': ['Rift-Medium'],
                'RiftBold': ['Rift-Bold'],
                'RiftItalic': ['Rift-Italic'],
                'RiftBoldItalic':['Rift-BoldItalic']
            },
    },
  },
  plugins: [],
}


