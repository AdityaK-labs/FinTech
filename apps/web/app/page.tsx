import Link from 'next/link';

export default function HomePage() {
  return (
    <main>
      <section className="card">
        <h1>AI Compliance SaaS</h1>
        <p>Automated GST, TDS and Income Tax intelligence for MSMEs and audit firms.</p>
        <Link href="/dashboard">Go to Dashboard</Link>
      </section>
    </main>
  );
}
