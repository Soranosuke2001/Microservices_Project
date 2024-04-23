import { NextRequest } from "next/server"

export async function GET(request: NextRequest) {
    try {
        const index = request.nextUrl.searchParams.get('index')

        const response = await fetch(process.env.PURCHASE_HISTORY_AUDIT_URL! + `?index=${index}`, { cache: 'no-store' })

        if (!response.ok) {
            return new Response(
                JSON.stringify({ message: "There was an error fetching data from Purchase History Audit Log Service"}),
                { status: 500 }
            )
        }

        const data = await response.json()

        if (!data) {
            return new Response(
                JSON.stringify("There was no data returned from the Purchase History Audit Log Service"),
                { status: 500 }
            )
        }

        return new Response(JSON.stringify({ message: data }), { status: 200 })
    } catch (err) {
        return new Response(
            JSON.stringify({ message: "There was an error fetching data"}),
            { status: 500 }
        )
    }
}