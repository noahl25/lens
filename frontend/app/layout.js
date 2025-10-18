import { Megrim } from "next/font/google";
import { Inter } from "next/font/google";
import "./globals.css";

export const megrim = Megrim({
  variable: "--font-megrim",
  subsets: ["latin"],
  weight: ["400"]
});

export const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"]
})

export const metadata = {
  title: "lens",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${megrim.className} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
