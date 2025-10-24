import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { cn } from "@/lib/utils"

export default function DashboardTable({ title, subtitle, headers, data }) {
    return (
        <Card className="pt-0 bg-black text-white border-white/20 border-2 col-span-1">
            <CardHeader className="flex items-center gap-2 space-y-0 border-b py-5 sm:flex-row">
                <div className="grid flex-1 gap-1">
                    <CardTitle>{title}</CardTitle>
                    <CardDescription>
                        {subtitle}
                    </CardDescription>
                </div>
            </CardHeader>
            <CardContent className="dark-scrollbar text-[2px]">
                <Table className="text-xs">
                    <TableHeader>
                        <TableRow>
                            <TableHead className="text-center"></TableHead>
                            {
                                headers.map((item, key) => (
                                    <TableHead key={key} className="text-center">{item}</TableHead>
                                ))
                            }
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((item, key) => (
                            <TableRow key={`row-${key}`}>
                                {
                                    item.map((val, key) => {
                                        return <TableCell key={`row-cell-${key}`} className={cn("font-medium", key === 0 ? "text-white text-left" : "text-white/50 text-center")}>{val}</TableCell>
                                    })
                                }
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent >
        </Card >
    )
}
