import React, { useState } from "react";
import "./CTFilter.scss";
import CTPopover from "../Popover/CTPopover";

const FILTER_TYPES = {
  Category: {
    selectMultiple: true,
    values: ["Category 1", "Category 2", "Category 3", "Category 4"],
  },
  Type: {
    selectMultiple: false,
    values: ["Type 1", "Type 2", "Type 3"],
  },
  Severity: {
    selectMultiple: false,
    values: ["Severity 1", "Severity 2", "Severity 3"],
  },
};

const CTFilter = (
  disabled = false,
  clearAllLabel = "Clear All",
  onChange,
  onClearAll,
  filterTypes = FILTER_TYPES,
  ...props
) => {
  const [activeFilters, setActiveFilters] = useState({});
  const [selectedFilter, setSelectedFilter] = useState("");

  const handleClearAll = () => {
    setSelectedFilter("");
    setActiveFilters({});
    // onClearAll();
  };

  const toggleFilter = (type, value) => {
    const _activeFilters = activeFilters;

    // removing a filter
    if (activeFilters[type] && activeFilters[type].includes(value)) {
      _activeFilters[type] = _activeFilters[type].filter((f) => f !== value);

      if (!_activeFilters[type].length) {
        delete _activeFilters[type];
      }
      setActiveFilters({ ..._activeFilters });
    }
    // adding a filter
    else {
      if (!_activeFilters[type]) {
        _activeFilters[type] = [];
      }

      if (filterTypes[selectedFilter].selectMultiple === true) {
        setActiveFilters({
          ...activeFilters,
          [type]: [..._activeFilters[type], value],
        });
      } else {
        setActiveFilters({ ...activeFilters, [type]: [value] });
      }
    }
  };

  const filterContent = (
    <div>
      <div>
        {selectedFilter !== "" ? (
          <span onClick={() => setSelectedFilter("")}>&#60;</span>
        ) : (
          ""
        )}
        <span>FILTERS</span>
        {/* Clear All */}
        {Object.keys(activeFilters).length > 0 && (
          <span onClick={handleClearAll}>{clearAllLabel}</span>
        )}
      </div>

      {/* List of filter values for a filter type */}
      {Object.keys(filterTypes).map((type, i) => (
        <div key={i}>
          {/* Top-level, showing filter type */}
          {selectedFilter === "" && (
            <div
              onClick={() => {
                if (disabled !== true) setSelectedFilter(type);
              }}
            >
              {type}
            </div>
          )}
          {/* This filter type's values */}
          {selectedFilter === type &&
            filterTypes[type].values.map((value, i) => (
              <div key={i} onClick={() => toggleFilter(type, value)}>
                {activeFilters[type] && activeFilters[type].includes(value) ? (
                  <span
                    className="iconify ct-filter-check-icon"
                    data-icon="mdi:check"
                    data-inline="false"
                  />
                ) : (
                  ""
                )}
                {value}
              </div>
            ))}
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
