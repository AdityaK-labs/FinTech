import { RiskCard } from '@/components/risk-card';

const metrics = [
  { label: 'Documents Processed', value: '2,134', helper: 'OCR + parsers' },
  { label: 'ITC Blocked', value: '₹4.8L', helper: 'Section 17(5) checks' },
  { label: 'Missed TDS Alerts', value: '17', helper: '194C / 194J / 194H' },
  { label: 'Filings Simulated', value: '86', helper: '26Q and GSTR-7' }
];

export default function DashboardPage() {
  return (
    <main>
      <h1>Compliance Command Center</h1>
      <div className="grid">
        {metrics.map((metric) => (
          <article key={metric.label} className="card">
            <h3>{metric.label}</h3>
            <p style={{ fontSize: '30px', margin: '4px 0' }}>{metric.value}</p>
            <small>{metric.helper}</small>
          </article>
        ))}
      </div>
      <RiskCard
        score={78}
        highRiskFlags={[
          'Turnover mismatch between GST and ITR',
          'Potential unsecured loan disclosure gap',
          'Advance tax underpayment trend'
        ]}
      />
    </main>
  );
}
