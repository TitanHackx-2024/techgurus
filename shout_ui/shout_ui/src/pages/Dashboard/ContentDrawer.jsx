import React, { useState } from "react";
import {
  Button,
  Drawer,
  IconButton,
  Input,
  Option,
  Select,
  Textarea,
  Typography,
} from "@material-tailwind/react";
import { useForm } from "react-hook-form";
import { MEDIA_TYPE } from "../../constants";
import MultiSelect from "react-select";
import makeAnimated from "react-select/animated";
import {toast} from "react-toastify";

export function ContentDrawer({ open, setOpen }) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm();
  const animatedComponents = makeAnimated();
  const [mediaType, setMediaType] = useState("");
  const [selectedPlatforms, setSelectedPlatform] = useState([]);
  const [fileData, setFileData] = useState(null);

  const platformOptions = [
    { value: 7, label: "LinkedIn" },
    { value: 6, label: "Spotify" },
    { value: 5, label: "Facebook" },
    { value: 4, label: "TikTok" },
    { value: 3, label: "Twitter" },
    { value: 2, label: "Instagram" },
    { value: 1, label: "YouTube" },
  ];

  return (
    <React.Fragment>
      {/*<Button onClick={()=> openDrawer}>Open Drawer</Button>*/}
      <Drawer
        open={open}
        onClose={() => setOpen(false)}
        className="p-4"
        placement={"right"}
        size={650}
      >
        <div className="mb-6 flex items-center justify-between">
          <Typography variant="h5" color="blue-gray">
            Upload Content
          </Typography>
          <IconButton
            variant="text"
            color="blue-gray"
            onClick={() => setOpen(false)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
              className="h-5 w-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </IconButton>
        </div>

        <form
          onSubmit={handleSubmit((data) => {
            console.log(fileData);
            const formData = new FormData();
            formData.append("title", data.title);
            formData.append("description", data.description);
            formData.append("text_content", data.text_content);
            formData.append("content_type", mediaType);
            formData.append("upload_status", "draft");
            formData.append("account_id", 1);
            formData.append("created_by", 1);
            formData.append("platforms", selectedPlatforms);
            formData.append("file", fileData);

              fetch(`${process.env.REACT_APP_BACKEND_URL}/content/`, {
                  method: "POST",
                  headers: {
                      "content-type": "multipart/form-data",
                  },
                  body: formData,
              }).then((res) => {
                  res.json().then(data => console.log(data))
              }).catch( err => {
                  toast.error("An error occurred. Please try after sometime.",{position:'top-center'});
              })
           })}
          className={"flex flex-col gap-4"}
        >
          <Input
            {...register("title", {
              required: "This is required",
              minLength: {
                value: 5,
                message: "Title cannot be less than 5 characters",
              },
            })}
            error={!!errors.title}
            label={errors?.title?.message || "Title"}
          />
          <Input
            {...register("description", {
              required: "Description is required",
              minLength: {
                value: 20,
                message: "Description cannot be less than 20 characters",
              },
            })}
            error={!!errors.description}
            label={errors?.description?.message || "Description"}
          />
          <Textarea
            {...register("text_content", {
              required: "Text content is required",
              minLength: {
                value: 50,
                message: "Text content cannot be less than 50 characters",
              },
            })}
            error={!!errors.text_content}
            label={errors?.text_content?.message || "Description"}
          />
          <Select
            error={getValues("title") !== "" && mediaType === ""}
            label={
              getValues("title") !== "" && mediaType === ""
                ? "Media is required"
                : "Select Media Type"
            }
            value={mediaType}
            onChange={(val) => setMediaType(val)}
          >
            {Object.keys(MEDIA_TYPE).map((type) => (
              <Option key={type} value={MEDIA_TYPE[type]}>
                {type}
              </Option>
            ))}
          </Select>
          {mediaType === MEDIA_TYPE.AUDIO && (
            <input
              type="file"
              id="soundFile"
              accept="audio/*"
              onChange={(e) => {
                console.log(e.target.files[0]);
              }}
            />
          )}
          {mediaType === MEDIA_TYPE.VIDEO && (
            <input
              type="file"
              id="videoFile"
              accept="video/*"
              onChange={(e) => {
                console.log(e.target.files[0]);
              }}
            />
          )}
          {mediaType === MEDIA_TYPE.IMAGE && (
            <input
              type="file"
              id="imageFile"
              accept="image/*"
              onChange={(e) => {
                console.log(e.target.files[0]);
              }}
            />
          )}{" "}
          {mediaType === MEDIA_TYPE.TEXT && (
            <input
              type="file"
              id="imageFile"
              accept="text/*"
              onChange={(e) => {
                console.log(e.target.files[0]);
              }}
            />
          )}
          <MultiSelect
            closeMenuOnSelect={false}
            components={animatedComponents}
            defaultValue={[]}
            isMulti
            options={platformOptions}
            onChange={(val) => setSelectedPlatform(val)}
          />
          <Button
            size="sm"
            type={"submit"}
            name="uploadFile"
            accept=""
            required
          >
            Submit
          </Button>
        </form>
      </Drawer>
    </React.Fragment>
  );
}
