import React from "react";

export default class UserHistory extends React.Component {
    constructor(props) {
        super(props);
        this.history = props.history || [];
    }
    
    renderUserHistory() {
        let result = [];
        for (let i = 0; i < this.history.length; i++) {
            result.push(
                <div key={i}>
                    <div style={{"display": "flex", "alignItems": "center", "justifyContent": "center"}}>
                      <div style={{"width": "70%"}}>
                          <pre style={{"maxHeight": "120px", "overflow":"auto", "display":"block"}}>
                              {this.history[i].query_string}
                          </pre>
                      </div>
                      <div style={{"display":"inline-block"}}>
                          <span style={{"marginLeft": "12px"}}>
                              {(new Date(this.history[i].executed_at * 1000)).toLocaleString()}
                          </span>
                      </div>
                    </div>
                    <hr/>
                </div>
            )
        }
        return result;
    }
    
    render() {
        return <div className="col-md-6" style={{"maxHeight": "75vh", "overflow": "auto"}}>
            <h2>Users history</h2>
            {this.renderUserHistory()}
        </div>
    }
    
}
