export default function Footer() {
  return (
    <footer className="bg-white border-t">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center space-x-6">
          <p className="text-center text-gray-500">
            © {new Date().getFullYear()} ASU Todo App. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
