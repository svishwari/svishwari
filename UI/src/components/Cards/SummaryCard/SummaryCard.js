import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import CountUp from "react-countup";

const useStyles = makeStyles((theme) => ({
  section: {
    display: "flex",
    flexDirection: "column",
    background: "#FFFFFF",
    border: "1px solid #D0D0CE",
    boxSizing: "border-box",
    borderRadius: "5px",
    width: "100%",
    padding: "10px",
    },
    title: {
        fontFamily: "Open Sans SemiBold",
        fontStyle: "normal",
        fontWeight: 600,
        fontSize: "12px",
        lineHeight: "16px",
        /* identical to box height, or 133% */
        
        letterSpacing: "0.2px",
        
        /* Text/ Light Gray */
        
        color: "#767676"
    },
    valueStyle: {
        fontFamily: "Open Sans SemiBold",
        fontStyle: "normal",
        fontWeight: 600,
        fontSize: "16px",
        lineHeight: "24px",
        /* identical to box height, or 133% */
        
        letterSpacing: "0.1px",
        
        /* Text/ Light Gray */
        
        color: "#333333"
  },
}));

const SummaryCard = (props) => {
  const classes = useStyles();
  return (
    <Paper elevation={3} className={classes.section}>
      {props.title ? <span className={classes.title}>{props.title}</span> : ""}
      <CountUp
        start={0}
        end={props.value}
        delay={0} {...props}
        className={classes.valueStyle}
      />
    </Paper>
  );
};

export default SummaryCard;
