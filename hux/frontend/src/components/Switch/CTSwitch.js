import { Switch } from '@material-ui/core';
import { withStyles } from '@material-ui/core/styles';
import React from 'react';

const CTSwitch = withStyles((theme) => ({
  root: {
    width: 57,
    height: 28,
    padding: 0,
  },
  switchBase: {
    padding: 1,
    '&$checked': {
      transform: 'translateX(34px)',
      left: -4,
      top: 3,
      color: theme.palette.common.white,
      '& + $track': {
        backgroundColor: '#0076A8',
        opacity: 1,
        border: 'none',
      },
    },
    '&$focusVisible $thumb': {
      color: '#52d869',
      border: '6px solid #fff',
    },
  },
  thumb: {
    width: 20,
    height: 20,
  },
  track: {
    borderRadius: 26 / 2,
    border: `1px solid ${theme.palette.grey[400]}`,
    backgroundColor: theme.palette.grey[50],
    opacity: 1,
    transition: theme.transitions.create(['background-color', 'border']),
  },
  label: {
    position: 'relative',
    left: -48,
    color: '#FFFFFF',
    fontSize: '0.85rem',
  },
  falseLabel: {
    position: 'relative',
    left: -28,
    fontSize: '0.85rem',
  },

  colorSecondary: {
    color: '#0076A8',
    top: 3,
    paddingLeft: 4,
  },
  switchWrap: {
    position: 'relative',
    display: 'inline-flex',
    alignItems: 'center',
    width: 60,
  },
  checked: {},
  focusVisible: {},
}))(({ classes, ...props }) => {
  const labelClass = props.checked ? classes.label : classes.falseLabel;
  return (
    <span className={classes.switchWrap}>
      <Switch
        focusVisibleClassName={classes.focusVisible}
        disableRipple
        classes={{
          root: classes.root,
          switchBase: classes.switchBase,
          thumb: classes.thumb,
          track: classes.track,
          checked: classes.checked,
          colorSecondary: classes.colorSecondary,
        }}
        {...props}
      />
      <span className={labelClass}>{props.label}</span>
    </span>
  );
});
export default CTSwitch;
