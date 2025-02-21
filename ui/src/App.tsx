import { useState } from "react"
import type { IFile } from "./types/file"
import FileCard from "./components/file_card"
import { Upload } from "lucide-react"
import { Button } from "@/components/ui/button"

function App() {
  const [files, setFiles] = useState<IFile[]>([
    {
      file_name: "sales_report.csv",
      file_description: "Monthly sales report with pivoted data",
      file_path: "/files/sales_report.csv",
    },
    {
      file_name: "users.jsonl",
      file_description: "Exported JSONL with user events",
      file_path: "/files/users.jsonl",
    },
  ])

  const handleUploadClick = () => {
    // Trigger file input or modal here
    alert("Upload triggered")
  }

  return (
    <div className='h-screen w-screen p-6 bg-gray-50'>
      <div className='flex h-full gap-6'>
        <div className='w-2/5 flex flex-col items-center justify-center'>
          <Button
            variant='outline'
            size='lg'
            className='flex flex-col items-center justify-center gap-2 py-8 px-4'
            onClick={handleUploadClick}
          >
            <Upload className='w-8 h-8 text-blue-600' />
            <span className='text-sm font-medium'>Upload File</span>
          </Button>
        </div>
        <div className='w-3/5 flex-1 overflow-y-auto'>
          <h2 className='text-xl font-semibold mb-4'>Your Files</h2>
          <div className='flex flex-col gap-4'>
            {files.map((file) => (
              <FileCard key={file.file_path} {...file} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
