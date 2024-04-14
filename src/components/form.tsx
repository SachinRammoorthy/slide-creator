import MultimodalInputList, { InputField, MultimodalInput } from "./input";
import { useState } from "react";

export default function InputForm() {
  const [title, setTitle] = useState<string>("");
  const [styles, setStyles] = useState<MultimodalInput[]>([]);
  const [topics, setTopics] = useState<MultimodalInput[]>([]);
  const [errors, setErrors] = useState<string[]>([]);

  function addInput(
    array: MultimodalInput[],
    setArray: (array: MultimodalInput[]) => void
  ) {
    const copy = [...array, { type: "", data: null }];
    setArray(copy);
  }

  function changeType(
    i: number,
    type: string,
    array: MultimodalInput[],
    setArray: (array: MultimodalInput[]) => void
  ) {
    const copy = array.slice();
    copy[i].type = type;
    setArray(copy);
  }

  function changeValue(
    i: number,
    data: string | FileList | null,
    array: MultimodalInput[],
    setArray: (array: MultimodalInput[]) => void
  ) {
    const copy = array.slice();
    copy[i].data = data;
    setArray(copy);
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

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setErrors([
      ...(styles
        .map((style, i) => validateMultimodalInput(`style input ${i}`, style))
        .filter((error) => error === null) as string[]),
      ...(topics
        .map((topic, i) => validateMultimodalInput(`topic input ${i}`, topic))
        .filter((error) => error === null) as string[]),
    ]);
    if (errors.length === 0) {
      console.log({
        title: title,
        styles: styles,
        topics: topics,
      });
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <InputField
        id="title"
        label="Title"
        type="text"
        value={title}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setTitle(e.target.value)
        }
      />
      <MultimodalInputList
        name="style"
        inputList={styles}
        addInput={() => addInput(styles, setStyles)}
        changeType={(i, type) => changeType(i, type, styles, setStyles)}
        changeValue={(i, data) => changeValue(i, data, styles, setStyles)}
      />
      <MultimodalInputList
        name="topic"
        inputList={topics}
        addInput={() => addInput(topics, setTopics)}
        changeType={(i, type) => changeType(i, type, topics, setTopics)}
        changeValue={(i, data) => changeValue(i, data, topics, setTopics)}
      />
      <input type="submit" />
    </form>
  );
}
