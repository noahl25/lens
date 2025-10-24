'use client'

import { Megrim } from "next/font/google";
import { Geist_Mono } from "next/font/google";
import Header from "@/components/Header";
import Threads from "@/components/Threads";
import { motion } from "motion/react";
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
    <html lang="en" className="bg-black">
      <body
        className={`${megrim.className} antialiased bg-black overflow-x-hidden`}
      >
        <Header />
        {children}
      </body>
    </html>
  );
}
