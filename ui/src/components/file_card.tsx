import type { IFile } from "../types/file"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { FileText, Download } from "lucide-react"

export default function FileCard({
  file_name,
  file_description,
  file_path,
}: IFile) {
  return (
    <Card className='w-full max-w-md shadow-md rounded-2xl p-4 flex items-start gap-4'>
      <div className='flex-shrink-0 mt-1'>
        <FileText className='h-6 w-6 text-blue-500' />
      </div>
      <CardContent className='p-0 flex-grow'>
        <h3 className='text-lg font-semibold'>{file_name}</h3>
        <p className='text-sm text-gray-500 mt-1 line-clamp-2'>
          {file_description}
        </p>
        <div className='mt-4 flex gap-2'>
          <a href={file_path} target='_blank' rel='noopener noreferrer'>
            <Button variant='outline' size='sm'>
              <Download className='h-4 w-4 mr-2' />
              Open
            </Button>
          </a>
        </div>
      </CardContent>
    </Card>
  )
}
