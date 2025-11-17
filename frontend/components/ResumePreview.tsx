interface ResumePreviewProps {
  sections: {
    product_owner?: string[];
    business_analyst?: string[];
    technical_ba?: string[];
    [key: string]: any;
  };
}

const SectionCard = ({ title, items }: { title: string; items?: string[] }) => (
  <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
    <h3 className="text-xl font-semibold text-gray-900">{title}</h3>
    {items && items.length > 0 ? (
      <ul className="mt-3 list-disc space-y-2 pl-5 text-gray-700">
        {items.map((item, index) => (
          <li key={`${title}-${index}`}>{item}</li>
        ))}
      </ul>
    ) : (
      <p className="mt-3 text-sm text-gray-500">No {title.toLowerCase()} content available.</p>
    )}
  </div>
);

const ResumePreview = ({ sections }: ResumePreviewProps) => {
  return (
    <div className="space-y-4">
      <SectionCard title="Product Owner" items={sections.product_owner} />
      <SectionCard title="Business Analyst" items={sections.business_analyst} />
      <SectionCard title="Technical BA" items={sections.technical_ba} />
    </div>
  );
};

export default ResumePreview;
