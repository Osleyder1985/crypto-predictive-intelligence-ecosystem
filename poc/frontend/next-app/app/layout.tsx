import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "CPIE Web POC — Next.js", description: "Prototipo sintético de investigación CPIE" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="es"><body>{children}</body></html>; }
