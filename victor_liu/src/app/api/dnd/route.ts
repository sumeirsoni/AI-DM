import { NextRequest, NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const category = searchParams.get("category");
    const index = searchParams.get("index");

    if (!category) {
      return NextResponse.json(
        { error: "Category parameter is required" },
        { status: 400 }
      );
    }

    const dndRawPath = join(process.cwd(), "dnd_raw");

    if (index) {
      const fileName = `${category}_${index.replace("/", "_")}.json`;
      const filePath = join(dndRawPath, fileName);

      try {
        const fileContent = await readFile(filePath, "utf-8");
        const data = JSON.parse(fileContent);
        return NextResponse.json(data);
      } catch (error) {
        return NextResponse.json({ error: "File not found" }, { status: 404 });
      }
    } else {
      const fileName = `${category}.json`;
      const filePath = join(dndRawPath, fileName);

      try {
        const fileContent = await readFile(filePath, "utf-8");
        const data = JSON.parse(fileContent);
        return NextResponse.json(data);
      } catch (error) {
        return NextResponse.json(
          { error: "Category not found" },
          { status: 404 }
        );
      }
    }
  } catch (error) {
    console.error("D&D API Error:", error);
    return NextResponse.json(
      {
        error: "Internal server error",
        message: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}
