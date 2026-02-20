export default function LoginPage() {
  return (
    <main>
      <section className="card">
        <span className="badge">Secure Onboarding</span>
        <h1>Autonomous Compliance Intelligence</h1>
        <p>Role-aware onboarding for Proprietor, MSME, and CA Firm users.</p>
        <form>
          <label>Email</label>
          <input type="email" placeholder="owner@company.in" style={{ width: '100%', margin: '8px 0 12px', padding: '10px' }} />
          <label>Password</label>
          <input type="password" placeholder="••••••••" style={{ width: '100%', margin: '8px 0 12px', padding: '10px' }} />
          <button type="submit" style={{ padding: '10px 14px' }}>Sign in</button>
        </form>
      </section>
    </main>
  );
}
