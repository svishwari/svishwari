import React from "react";
import CTPrimaryButton from "../Button/CTPrimaryButton";
import "./CTDataGridTop.scss";
import CTFilter from "../Filter/CTFilter";

// TO DO ITEMS CHANGE FILTER COMPONENT
const CTDataGridTop = ({
  onSearch,
  onAddClick,
  onRemove,
  onDownload,
  selectedRows,
  pageName = "Audience",
  changeEditing,
  isEditing = false,
}) => (
  <div className="ct-grid-top-wrapper">
    <span className="ct-grid-top-left">
      <span
        className="iconify ct-grid-search"
        data-icon="mdi:search"
        data-inline="false"
      />
      <input
        onChange={(e) => {
          onSearch(e);
        }}
        className="ct-grid-search-input"
        placeholder="Search"
      />
    </span>
    <span className="ct-grid-top-right">
      <span className="ct-grid-icon-buttons">
        {isEditing ? (
          <>
            <button type="button" onClick={() => onDownload(selectedRows)}>
              <span
                className="iconify"
                data-icon="mdi:smile"
                data-inline="false"
              />
            </button>
            <button type="button" onClick={() => onRemove(selectedRows)}>
              <span
                className="iconify"
                data-icon="mdi:delete"
                data-inline="false"
              />
              <span className="ct-grid-remove-text">Remove</span>
            </button>
          </>
        ) : (
          <>
            <button type="button" onClick={() => changeEditing()}>
              <span
                className="iconify"
                data-icon="mdi:pencil"
                data-inline="false"
              />
            </button>
          </>
        )}
        <button type="button" >
          <CTFilter />
        </button>
      </span>
      {isEditing ? (
        <CTPrimaryButton onClick={() => changeEditing()}>
          Done &amp; Return
        </CTPrimaryButton>
      ) : (
        <CTPrimaryButton onClick={() => onAddClick()}>
          {`+ ${pageName}`}
        </CTPrimaryButton>
      )}
    </span>
  </div>
);

export default CTDataGridTop;
