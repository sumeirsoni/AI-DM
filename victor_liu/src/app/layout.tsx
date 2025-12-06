import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "D&D 5e Data Viewer",
  description: "D&D 5e data viewer with text-to-speech",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

