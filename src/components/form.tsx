import { useState } from "react";

interface InputFieldProps {
  id: string;
  type: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

function InputField({ id, type, value, onChange }: InputFieldProps) {
  return (
    <input name={id} id={id} type={type} onChange={onChange} value={value} />
  );
}

interface DropdownFieldProps {
  id: string;
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
}

function DropdownField({ id, onChange }: DropdownFieldProps) {
  return (
    <select name={id} id={id} onChange={onChange}>
      <option value=""></option>
      <option value="text">Text</option>
      <option value="video">Video</option>
      <option value="audio">Audio</option>
    </select>
  );
}

interface MultimodalInput {
  type: string;
  data: FileList | string | null;
}

interface MultimodalInputFieldProps {
  id: string;
  value: MultimodalInput;
  onTypeChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  onValueChange: (e: React.ChangeEvent<HTMLInputElement>, t: string) => void;
}

function MultimodalInputField({
  id,
  value,
  onTypeChange,
  onValueChange,
}: MultimodalInputFieldProps) {
  function mapType(type: string) {
    if (type === "text")
      return (
        <InputField
          id={id}
          type="text"
          value={value.data as string}
          onChange={(e) => onValueChange(e, type)}
        />
      );
    else if (type === "video" || type === "audio") {
      return (
        <InputField
          id={id}
          type="file"
          onChange={(e) => onValueChange(e, type)}
        />
      );
    } else return <div className="hidden"> </div>;
  }
  return (
    <div id={id}>
      <DropdownField id={`form${id}`} onChange={onTypeChange} />
      {mapType(value.type)}
    </div>
  );
}

export default function InputForm() {
  const [title, setTitle] = useState<string>("");
  const [topic, setTopic] = useState<MultimodalInput>({ type: "", data: "" });
  const [style, setStyle] = useState<MultimodalInput>({ type: "", data: "" });
  const [errors, setErrors] = useState<string[]>([]);

  function handleTitleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setTitle(e.target.value);
  }

  function handleMultimodalTypeChange(
    e: React.ChangeEvent<HTMLSelectElement>,
    value: MultimodalInput,
    setter: React.Dispatch<React.SetStateAction<MultimodalInput>>
  ) {
    const type = e.target.value;
    setter({ type: type, data: "" });
  }

  function handleMultimodalValueChange(
    e: React.ChangeEvent<HTMLInputElement>,
    setter: React.Dispatch<React.SetStateAction<MultimodalInput>>,
    type: string
  ) {
    if (type === "text") {
      setter({ type: type, data: e.target.value });
    } else if (type === "video" || type === "audio") {
      setter({ type: type, data: e.target.files! });
    } else {
      setter({ type: type, data: "" });
    }
  }

  function validateMultimodalInput(name: string, value: MultimodalInput) {
    let header = `Error in ${name}: `;
    if (value.type === "") {
      return header + "Must select an input type";
    } else if (value.type === "text") {
      if (value.data === "") {
        return header + "Text input cannot be empty";
      }
    } else if (value.type === "video" || value.type === "audio") {
      if (value.data === null || value.data.length === 0) {
        return header + "File input cannot be empty";
      }
    }
    return null;
  }

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErrors([]);

    if (title === "") {
      setErrors((prev) => [...prev, "Title cannot be empty"]);
    }

    const styleError = validateMultimodalInput("style", style);
    if (styleError !== null) {
      setErrors((prev) => [...prev, styleError]);
    }
    const topicError = validateMultimodalInput("topic", topic);
    if (topicError !== null) {
      setErrors((prev) => [...prev, topicError]);
    }
  }

  return (
    <div>
      <form onSubmit={onSubmit}>
        <label htmlFor="formTitle">Title</label>
        <InputField
          id="formTitle"
          type="text"
          value={title}
          onChange={handleTitleChange}
        />
        <label htmlFor="style">Style</label>
        <MultimodalInputField
          id="style"
          value={style}
          onTypeChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            handleMultimodalTypeChange(e, style, setStyle)
          }
          onValueChange={(
            e: React.ChangeEvent<HTMLInputElement>,
            type: string
          ) => handleMultimodalValueChange(e, setStyle, type)}
        />
        <label htmlFor="topic">Topic</label>
        <MultimodalInputField
          id="topic"
          value={topic}
          onTypeChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            handleMultimodalTypeChange(e, topic, setTopic)
          }
          onValueChange={(
            e: React.ChangeEvent<HTMLInputElement>,
            type: string
          ) => handleMultimodalValueChange(e, setTopic, type)}
        />
        <button type="submit">Submit</button>
      </form>
      <div>
        {errors.map((error) => (
          <p key={error.split(":")[0]}>{error}</p>
        ))}
      </div>
    </div>
  );
}
