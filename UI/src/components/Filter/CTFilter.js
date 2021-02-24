/* eslint-disable jsx-a11y/click-events-have-key-events */
import React, { useState } from "react";
import "./CTFilter.scss";
import CTPopover from "../Popover/CTPopover";


// THIS IS A TODO FILE
// MOST OF THE FUNCTIONALITY STILL NEEDS TO BE CHANGED
const CTFilter = (props) => {

  const [activeFilters, setActiveFilters] = useState({});
  const [selectedFilter, setSelectedFilter] = useState("");

  const handleClearAll = () => {
    setSelectedFilter("");
    setActiveFilters({});

    props.onClearAll();
  }

  const toggleFilter = (type, value) => {
    const _activeFilters = activeFilters;

    // removing a filter
    if (activeFilters[type] && activeFilters[type].includes(value)) {
      _activeFilters[type] = _activeFilters[type].filter(f => f !== value)

      if (!_activeFilters[type].length) { delete _activeFilters[type] }
      setActiveFilters({..._activeFilters})
    }
    // adding a filter
    else {
      if (!_activeFilters[type]) { _activeFilters[type] = [] }
    
      if (props.filterTypes[selectedFilter].selectMultiple === true) {
        setActiveFilters({...activeFilters, [type]: [..._activeFilters[type], value]})
      } else {
        setActiveFilters({...activeFilters, [type]: [value]})
      }
    }
  }

  const filterContent = (
    <div>
      {/* Go up to the filter types list */}
      <span onClick={() => setSelectedFilter("")}>
        { selectedFilter && '<' }
        {props.label.toUpperCase()}
        {Object.keys(activeFilters).length > 0 && ` (${Object.keys(activeFilters).length})`}
      </span>

      {/* Clear All */}
      { Object.keys(activeFilters).length > 0 && <span onClick={handleClearAll}>{props.clearAllLabel}</span> }

      {/* List of filter values for a filter type */}
      {Object.keys(props.filterTypes).map((type) => (
        <div>
          {/* Top-level, showing filter type */}
          {!selectedFilter && 
            <div onClick={() => { if (props.disabled !== true) setSelectedFilter(type) }}>
              {type}
            </div>
          }
        
          {/* This filter type's values */}
          {selectedFilter === type && props.filterTypes[type].values.map(value => (
            <div onClick={() => toggleFilter(type, value)}>
              {activeFilters[type] && activeFilters[type].includes(value) && <span>Tick</span>}
              {value}
            </div>
          ))
          }
        </div>
      ))}
    </div>
  );

  return (
    <CTPopover popoverContent={filterContent}>
      <div className="ct-filter-wrapper">
        <span className="iconify" data-icon="mdi:filter" data-inline="false" />
      </div>
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