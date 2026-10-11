import { type FieldDefinition } from "@/api/entityApi"
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Trash2, ChevronUp, ChevronDown } from "lucide-react"

const FIELD_TYPES = [
  { value: "text", label: "Текст" },
  { value: "textarea", label: "Многострочный" },
  { value: "number", label: "Число" },
  { value: "date", label: "Дата" },
  { value: "select", label: "Выбор" },
  { value: "multiselect", label: "Множественный выбор" },
  { value: "boolean", label: "Чекбокс" },
  { value: "url", label: "Ссылка" },
  { value: "email", label: "Email" },
]

interface FieldEditorProps {
  field: FieldDefinition
  index: number
  onChange: (field: FieldDefinition) => void
  onDelete: () => void
  onMoveUp: () => void
  onMoveDown: () => void
  canMoveUp: boolean
  canMoveDown: boolean
}

export function FieldEditor({
  field,
  index,
  onChange,
  onDelete,
  onMoveUp,
  onMoveDown,
  canMoveUp,
  canMoveDown,
}: FieldEditorProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>{index + 1}. {field.key}</span>
          <div className="flex gap-1">
            <Button
              variant="ghost"
              size="icon"
              disabled={!canMoveUp}
              onClick={onMoveUp}
            >
              <ChevronUp className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              disabled={!canMoveDown}
              onClick={onMoveDown}
            >
              <ChevronDown className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={onDelete}>
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Key */}
        <div>
          <Label>Ключ поля (key)</Label>
          <Input
            value={field.key}
            onChange={(e) => {
              const v = e.target.value
              if (/^[a-zA-Z0-9_]*$/.test(v)) {
                onChange({ ...field, key: v })
              }
            }}
            placeholder="field_name"
          />
        </div>

        {/* Label */}
        <div>
          <Label>Название поля</Label>
          <Input
            value={field.label}
            onChange={(e) => onChange({ ...field, label: e.target.value })}
          />
        </div>

        {/* Description */}
        <div>
          <Label>Описание</Label>
          <Input
            value={field.description ?? ""}
            onChange={(e) => onChange({ ...field, description: e.target.value })}
            placeholder="Описание поля"
          />
        </div>

        {/* Type */}
        <div>
          <Label>Тип</Label>
          <Select
            value={field.type}
            onValueChange={(v) => onChange({ ...field, type: v })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {FIELD_TYPES.map((t) => (
                <SelectItem key={t.value} value={t.value}>
                  {t.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Required */}
        <div className="flex items-center gap-2">
          <Checkbox
            checked={field.required}
            onCheckedChange={(v) =>
              onChange({ ...field, required: !!v })
            }
          />
          <Label>Обязательное</Label>
        </div>

        {/* Default */}
        {["text", "number", "textarea", "url", "email"].includes(field.type) && (
          <div>
            <Label>Значение по умолчанию</Label>
            <Input
              value={field.default ?? ""}
              onChange={(e) => {
                const v = e.target.value
                onChange({
                  ...field,
                  default: field.type === "number" ? (v === "" ? undefined : Number(v)) : v,
                })
              }}
              placeholder="Значение по умолчанию"
              type={field.type === "number" ? "number" : "text"}
            />
          </div>
        )}

        {/* Options */}
        {(field.type === "select" || field.type === "multiselect") && (
          <div>
            <Label>Варианты (через запятую)</Label>
            <Input
              value={field.options?.join(", ")}
              onChange={(e) =>
                onChange({
                  ...field,
                  options: e.target.value
                    .split(",")
                    .map((s) => s.trim())
                    .filter(Boolean),
                })
              }
              placeholder="Вариант 1, Вариант 2, ..."
            />
          </div>
        )}
      </CardContent>
    </Card>
  )
}
