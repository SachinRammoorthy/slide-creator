export interface MultimodalInput {
  type: string;
  data: File | string | null;
}

interface InputFieldProps {
  id: string;
  label: string;
  type: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export function InputField({
  id,
  label,
  type,
  value,
  onChange,
}: InputFieldProps) {
  return (
    <div>
      <label className="mt-3 " htmlFor={id}>
        {label}
      </label>
      <input
        className="text-black"
        name={id}
        id={id}
        type={type}
        onChange={onChange}
        value={value}
      />
    </div>
  );
}

interface MultimodalInputFieldProps {
  name: string;
  value: MultimodalInput;
  onTypeChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  onValueChange: (e: React.ChangeEvent<HTMLInputElement>, t: string) => void;
}

export function MultimodalInputField({
  name,
  value,
  onTypeChange,
  onValueChange,
}: MultimodalInputFieldProps) {
  function mapType(type: string) {
    if (type === "text")
      return (
        <InputField
          id={`${name}Input`}
          label="Prompt Text"
          type="text"
          value={value.data as string}
          onChange={(e) => onValueChange(e, type)}
        />
      );
    else if (type === "video" || type === "audio") {
      return (
        <InputField
          id={`${name}Input`}
          label={type.charAt(0).toUpperCase() + type.slice(1) + " File"}
          type="file"
          onChange={(e) => onValueChange(e, type)}
        />
      );
    } else return <div className="hidden"> </div>;
  }
  return (
    <div id={name}>
      <select id={`${name}Select`} onChange={onTypeChange}>
        <option value="">~Input Type~</option>
        <option value="text">Text</option>
        <option value="video">Video</option>
        <option value="audio">Audio</option>
      </select>
      {mapType(value.type)}
    </div>
  );
}

interface MultimodalInputListProps {
  name: string;
  inputList: MultimodalInput[];
  addInput: () => void;
  changeType: (i: number, type: string) => void;
  changeValue: (i: number, data: string | File | null) => void;
}

export default function MultimodalInputList({
  name,
  inputList,
  addInput,
  changeType,
  changeValue,
}: MultimodalInputListProps) {
  return (
    <div>
      <h1>{name}</h1>
      {inputList.map((input: MultimodalInput, i: number) => (
        <MultimodalInputField
          key={i}
          name={`${name}Input${i}`}
          value={input}
          onTypeChange={(e) => {
            changeType(i, e.target.value);
          }}
          onValueChange={(e, type) => {
            const data = type === "text" ? e.target.value : e.target.files![0];
            changeValue(i, data);
          }}
        />
      ))}
      <button type="button" onClick={addInput}>
        Add Input
      </button>
    </div>
  );
}
