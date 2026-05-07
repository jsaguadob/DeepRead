export default function LoadingSkeleton() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-cream-50">
      <div className="text-center">
        <div className="animate-spin h-10 w-10 border-4 border-ember-500 border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-deepnavy-400 font-medium">Cargando DeepRead...</p>
      </div>
    </div>
  );
}
