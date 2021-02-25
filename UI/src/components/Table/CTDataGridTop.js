import React, { useState } from "react";
import CTPrimaryButton from "../Button/CTPrimaryButton";
import "./CTDataGridTop.scss";
import CTFilter from "../Filter/CTFilter";
import CTSecondaryButton from "../Button/CTSecondaryButton";

// TO DO ITEMS CHANGE FILTER COMPONENT
const CTDataGridTop = ({
  onSearch,
  onAddClick,
  onRemove,
  onDownload,
  selectedRows,
  pageName,
  changeEditing,
  isEditing,
  isSummaryEnabled,
  onSummaryToggle,
  isDownloadAble,
  bulkOperationText,
  onBulkOperation,
  onFilterChange,
  onClearAll,
  filterTypes,
}) => {
const [gridTopState,setGridTopState] = useState({
  isSummaryHidden: true,
  isUserEditing: isEditing,
});

const toggleSummary = () => {
  setGridTopState(prevState => ({
    ...prevState,
    isSummaryHidden: !prevState.isSummaryHidden,
  }))
  onSummaryToggle()
}

const toggleEditing = () => {
  setGridTopState(prevState => ({
    ...prevState,
    isUserEditing: !prevState.isUserEditing,
  }))
  changeEditing();
}

return (
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
        placeholder={`Search ${pageName}s`}
      />
    </span>
    <span className="ct-grid-top-right">
      <span className="ct-grid-icon-buttons">
        {gridTopState.isUserEditing ? (
          <>
            { isDownloadAble && 
              <button type="button" onClick={() => onDownload(selectedRows)}>
                <span
                  className="iconify"
                  data-icon="mdi:download"
                  data-inline="false"
                />
              </button>
            }
            <button type="button" onClick={() => onRemove()}>
              <span
                className="iconify"
                data-icon="mdi:delete"
                data-inline="false"
              />
              <span className="ct-grid-remove-text">Remove</span>
            </button>
            { bulkOperationText !=="" && 
              <CTSecondaryButton onClick={() => onBulkOperation(selectedRows)}>{bulkOperationText}</CTSecondaryButton>
            }
          </>
        ) : (
          <>
            <button type="button" onClick={() => toggleEditing()}>
              <span
                className="iconify"
                data-icon="mdi:pencil"
                data-inline="false"
              />
            </button>
          </>
        )}
        <button type="button" >
          <CTFilter filterTypes={filterTypes} onFilterChange={onFilterChange} onClearAll={onClearAll}/>
        </button>
      </span>
      <span className="ct-grid-summary">
        {isSummaryEnabled && !gridTopState.isUserEditing ?
            gridTopState.isSummaryHidden ? (
              <CTSecondaryButton  onClick={toggleSummary}>Show Summary</CTSecondaryButton>
            ):(
              <CTPrimaryButton onClick={toggleSummary}>Hide Summary</CTPrimaryButton>
            ):(
            <></>
        )}
      </span>
      {gridTopState.isUserEditing ? (
        <CTPrimaryButton onClick={() => toggleEditing()}>
          Done &amp; Return
        </CTPrimaryButton>
      ) : (
        <CTPrimaryButton onClick={() => onAddClick()}>
          {`+ ${pageName}`}
        </CTPrimaryButton>
      )}
    </span>
  </div>
)};

export default CTDataGridTop;
