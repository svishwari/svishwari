/* eslint-disable jsx-a11y/click-events-have-key-events */
import React, { useState } from "react";
import "./CTFilter.scss";
import Badge from '@material-ui/core/Badge';
import CTPopover from "../Popover/CTPopover";

// THIS IS A TODO FILE
// MOST OF THE FUNCTIONALITY STILL NEEDS TO BE CHANGED
const CTFilter = ({
    label="Filters",
    clearAllLabel="Clear All",
    filterTypes={},
    onFilterChange=()=>{},
    onClearAll=()=>{},
  }) => {

  const [activeFilters, setActiveFilters] = useState({});
  const [selectedFilter, setSelectedFilter] = useState("");
  const handleClearAll = () => {
    setSelectedFilter("");
    setActiveFilters({});
    onClearAll();
  }

  const toggleFilter = (type, value) => {
    let _activeFilters = {...activeFilters};

    // removing a filter
    if (activeFilters[type] && activeFilters[type].includes(value)) {
      _activeFilters[type] = _activeFilters[type].filter(f => f !== value)

      if (!_activeFilters[type].length) { delete _activeFilters[type] }
      setActiveFilters({..._activeFilters})
    }
    // adding a filter
    else {
      if (!_activeFilters[type]) { _activeFilters[type] = [] }

      if (filterTypes[selectedFilter].selectMultiple === true) {
        _activeFilters = {..._activeFilters, [type]: [..._activeFilters[type], value]}
        setActiveFilters(_activeFilters)
      } else {
        _activeFilters = {..._activeFilters, [type]: [value]}
        setActiveFilters(_activeFilters)
      }
    }
    onFilterChange(_activeFilters);
  }

  const filterContent = (
    <div className="ct-filter-popover-wrapper">
      <div className="ct-filter-header">
        <span onClick={() => setSelectedFilter("")} className="ct-filter-header-left">
          {selectedFilter &&  <span>&lt; </span>}
          {label.toUpperCase()}
          { Object.keys(activeFilters).length > 0 &&  ` (${Object.keys(activeFilters).length})`}
        </span>
        <span className="ct-filter-header-right">
          <span onClick={handleClearAll}>{clearAllLabel}</span>
        </span>
      </div>

      <div className="ct-filter-content">
        {
          selectedFilter === ""
          ?
            Object.keys(filterTypes).map( (type) => (
            <div key={type} className="ct-filter-content-card" onClick={() => setSelectedFilter(type)}>
              <span>{type}{activeFilters[type] &&  ` (${activeFilters[type].length})`}</span>
              <span>&gt;</span>
            </div>
            ))
          :
          (<div>
            <div className="ct-filter-title">{selectedFilter.toUpperCase()}</div>
            <div className="ct-filter-type-container">
            {
              filterTypes[selectedFilter].values.map(value => (
                <div className="ct-filter-type" key={value} onClick={() => toggleFilter(selectedFilter, value)}>
                  { activeFilters[selectedFilter] && activeFilters[selectedFilter].includes(value)
                  && <span><span className="iconify" data-icon="mdi:check" data-inline="false"/></span>}
                  {value}
                </div>
              ))
            }
            </div>
          </div>)
        }
      </div>

    </div>
  );

  return (
    <CTPopover onToggle={()=> setSelectedFilter("")} customClass="ct-filter-popover" popoverContent={filterContent}>
      <button type="button">
        <div className="ct-filter-wrapper">
          <Badge badgeContent={Object.keys(activeFilters).length}>
            <span className="ct-filter-icon">
              <span className="iconify" data-icon="mdi:filter" data-inline="false" />
            </span>
          </Badge>
        </div>
      </button>
    </CTPopover>
  );
};

export default CTFilter;

CTFilter.defaultProps = {
  open: true,
  disabled: false,
  label: 'Filters',
  clearAllLabel: 'Clear All',
}
