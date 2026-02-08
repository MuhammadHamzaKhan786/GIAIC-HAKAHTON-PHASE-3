export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 py-8">
      <div className="container mx-auto px-4 text-center">
        <p className="text-gray-500">
          © {new Date().getFullYear()} Todo CLI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}