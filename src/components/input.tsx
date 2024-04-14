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
      <label className="mr-3 text-white" htmlFor={id}>
        {label}
      </label>
      <input name={id} id={id} type={type} onChange={onChange} value={value} />
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
    <div className="grid grid-flow-col" id={name}>
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
    <div className="my-5">
      <h1 className="text-white font-bold text-3xl">
        Set {name[0].toUpperCase() + name.slice(1)} Features
      </h1>
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
      <button
        type="button"
        className="text-white my-3 px-3 bg-slate-500 border-2 hover:text-white hover:bg-slate-700 border-slate-500 rounded transition:all duration-300 ease-in-out"
        onClick={addInput}
      >
        Add Input
      </button>
    </div>
  );
}
