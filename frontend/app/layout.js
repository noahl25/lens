import { Megrim } from "next/font/google";
import { Geist_Mono } from "next/font/google";
import Header from "@/components/Header";
import "./globals.css";

export const megrim = Megrim({
  variable: "--font-megrim",
  subsets: ["latin"],
  weight: ["400"]
});

export const fontBasic = Geist_Mono({
  variable: "--font-basic",
  subsets: ["latin"]
})

const metadata = {
  title: "lens",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${megrim.className} antialiased`}
      >
        <Header />
        {children}
      </body>
    </html>
  );
}
