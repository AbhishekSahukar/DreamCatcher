export default function InterpretationBubble({ text }) {
  return (
    <div className="w-full max-w-3xl mt-8 bg-white bg-opacity-20 backdrop-blur p-6 rounded-2xl shadow-md text-white text-lg leading-relaxed">
      <h2 className="text-2xl font-semibold mb-4">🌙 Your Dream Meaning</h2>
      <p>{text}</p>
    </div>
  );
}
