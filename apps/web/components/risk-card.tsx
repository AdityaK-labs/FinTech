interface RiskCardProps {
  score: number;
  highRiskFlags: string[];
}

export function RiskCard({ score, highRiskFlags }: RiskCardProps) {
  return (
    <section className="card">
      <h3>Compliance Risk Score™</h3>
      <p style={{ fontSize: '36px', margin: '8px 0' }}>{score}/100</p>
      <ul>
        {highRiskFlags.map((flag) => (
          <li key={flag}>{flag}</li>
        ))}
      </ul>
    </section>
  );
}
