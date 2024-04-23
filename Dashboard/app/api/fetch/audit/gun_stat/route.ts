import { NextRequest } from "next/server"

export async function GET(request: NextRequest) {
    try {
        const index = request.nextUrl.searchParams.get('index')

        console.log(`Index Value: ${index}`)

        const response = await fetch(process.env.GUN_STAT_AUDIT_URL! + `?index=${index}`, { cache: 'no-store' })

        if (!response.ok) {
            return new Response(
                JSON.stringify({ message: "There was an error fetching data from Gun Stat Audit Log Service"}),
                { status: 500 }
            )
        }

        const data = await response.json()

        if (!data) {
            return new Response(
                JSON.stringify("There was no data returned from the Gun Stat Audit Log Service"),
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