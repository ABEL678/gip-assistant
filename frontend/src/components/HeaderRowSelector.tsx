import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface HeaderRowSelectorProps {
  previewRows: unknown[][]
  selectedIndex: number
  onSelect: (index: number) => void
}

export function HeaderRowSelector({
  previewRows,
  selectedIndex,
  onSelect,
}: HeaderRowSelectorProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Выберите строку с заголовками</CardTitle>
        <p className="text-sm text-muted-foreground">
          Мы предположили строку {selectedIndex + 1}. Если это не так — укажите
          вручную. Заголовки — это строка, где написаны названия колонок
          («Тип», «Элемент», «Дата выдачи» и т.д.)
        </p>
      </CardHeader>
      <CardContent>
        <RadioGroup
          value={String(selectedIndex)}
          onValueChange={(v) => onSelect(Number(v))}
          className="space-y-2"
        >
          {previewRows.map((row, idx) => {
            const isSelected = idx === selectedIndex
            const nonEmpty = row.filter(
              (c) => c !== null && c !== undefined && String(c).trim() !== "",
            ).length

            if (nonEmpty === 0) return null // пропускаем пустые строки

            return (
              <div
                key={idx}
                className={`
                  flex items-start gap-3 p-3 rounded-md border
                  ${isSelected ? "border-primary bg-primary/5" : "border-border"}
                `}
              >
                <RadioGroupItem value={String(idx)} id={`header-row-${idx}`} />
                <Label
                  htmlFor={`header-row-${idx}`}
                  className="flex-1 cursor-pointer"
                >
                  <div className="text-xs text-muted-foreground mb-1">
                    Строка {idx + 1} ({nonEmpty} заполненных ячеек)
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {row
                      .filter(
                        (c) => c !== null && c !== undefined && String(c).trim() !== "",
                      )
                      .slice(0, 15)
                      .map((cell, i) => (
                        <span
                          key={i}
                          className="inline-block px-2 py-0.5 text-xs bg-muted rounded"
                        >
                          {String(cell).slice(0, 40)}
                        </span>
                      ))}
                    {nonEmpty > 15 && (
                      <span className="text-xs text-muted-foreground">
                        +{nonEmpty - 15} ещё
                      </span>
                    )}
                  </div>
                </Label>
              </div>
            )
          })}
        </RadioGroup>
      </CardContent>
    </Card>
  )
}