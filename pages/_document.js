import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        <link rel="icon" type="image/x-icon" href="/images/logo.png" />
        <link rel="stylesheet" href="/css/style.css" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Krona+One&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet" />
        <link rel="stylesheet" href="/css/index.css" />
        <style>{`
          .page__container {
            background-image: url("/svg/page.png") !important;
          }
          .page__container::after {
            background-image: url("/svg/components.svg") !important;
          }
        `}</style>
      </Head>
      <body 
        data-version="2.2" 
        onContextMenu={(e) => e.preventDefault()} 
        onSelectStart={(e) => e.preventDefault()} 
        onDragStart={(e) => e.preventDefault()}
      >
        <Main />
        <NextScript />
        <script src="/js/html_version.js"></script>
        <script src="/js/script.js"></script>
        <script src="/js/scroll.js"></script>
      </body>
    </Html>
  )
}