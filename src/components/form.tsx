import MultimodalInputList, { InputField, MultimodalInput } from "./input";
import { useState } from "react";
import axios from "axios";

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
    data: string | File | null,
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
      if (value.data === null) {
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
        .filter((error) => error != null) as string[]),
      ...(topics
        .map((topic, i) => validateMultimodalInput(`topic input ${i}`, topic))
        .filter((error) => error != null) as string[]),
    ]);

    const data = JSON.stringify({
      title: title,
      styles: styles.map((style) => {
        if (style.type !== "text") {
          return {
            type: style.type,
            data: (style.data as File).name,
          };
        }
        return style;
      }),
      topics: topics.map((topic) => {
        if (topic.type !== "text") {
          return {
            type: topic.type,
            data: (topic.data as File).name,
          };
        }
        return topic;
      }),
    });

    const request = new FormData();
    request.append("data", data);

    for (let i = 0; i < styles.length; i++) {
      if (styles[i].type !== "text" && styles[i].data !== null) {
        request.append((styles[i].data as File).name, styles[i].data as File);
      }
    }

    for (let i = 0; i < topics.length; i++) {
      if (topics[i].type !== "text" && topics[i].data !== null) {
        request.append((topics[i].data as File).name, topics[i].data as File);
      }
    }

    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };

    axios
      .post("http://localhost:8000/generate/", request, config)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error uploading files: ", error);
      });
  }

  return (
    <div>
      <form onSubmit={handleSubmit} className="max-w-md mx-auto">
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
        <input
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        />
      </form>
      <div>
        {errors.map((error, i) => (
          <div key={i}>{error}</div>
        ))}
      </div>
    </div>
  );
}
