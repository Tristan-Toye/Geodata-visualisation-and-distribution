import plotly
from flask import Flask, render_template, Response
from pykafka import KafkaClient
from plotly import graph_objs as go
import json

y_waarden=[]
key=[]
tijd = []


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

app = Flask(__name__)

@app.route('/DataMonitoring_Elektrische_Wagen')
def index():
    return(render_template('index.html'))


#Consumer API
@app.route('/DataMonitoring_Elektrische_Wagen/geo_spatial_data')
def get_messages_map():
    client = get_kafka_client()
    def events_map():
        consumer = client.topics['geo_spatial_data'].get_simple_consumer(
        consumer_group="geo_data",
        auto_commit_enable=True,
        auto_commit_interval_ms= 1000,
        auto_offset_reset=OffsetType.LATEST,
        reset_offset_on_start=False
        )
        for message in consumer:
             yield 'data:{0}\n\n'.format(message.value.decode())
    return Response(events_map(), mimetype="text/event-stream")


@app.route('/DataMonitoring_Elektrische_Wagen/grafiek')
def get_messages_grafiek():
        client= get_kafka_client()
        def events_grafiek():
            consumer = client.topics['geo_spatial_data'].get_simple_consumer(
            consumer_group="grafiek",
            auto_commit_enable=True,
            auto_commit_interval_ms= 1000,
            auto_offset_reset=OffsetType.LATEST,
            reset_offset_on_start=False
            )
            for message in consumer:
                data_gelezen = json.loads(message.value.decode())
                y_waarden.append(data_gelezen['snelheid'])
                if len(y_waarden) >= 20:
                    laatstegetallen = y_waarden[len(y_waarden)-20:]
                else:
                    laatstegetallen = y_waarden
                key.append(str(data_gelezen['key']))
                tijd.append("UTC:"+str(data_gelezen['tijd']))
                afgelegde_weg = data_gelezen['afgelegde_weg']

                grafiek = {'data':json.dumps([go.Scatter(
                x0 = 0,
                dx = 1,
                y = y_waarden,
                name = str(data_gelezen['auto']),
                visible=True,
                showlegend=True,
                opacity=1,
                mode='lines+markers',
                ids=key,
                hoverinfo='x+y+text',
                hovertext=tijd,
                hoveron='points',
                textposition='top center',

                marker=dict(
                symbol='circle-open',
                size=7,
                color='rgba(0,0,102,1)'
                ),

                line=dict(
                color='rgba(0,0,204,1)',
                width=3,
                shape='spline',
                smoothing=1.3,
                dash='solid',
                simplify=False
                ),

                hoverlabel=dict(
                bgcolor='rgba(255,255,255,1)',
                bordercolor='rgba(0,0,128,1)',
                align='auto',
                namelength=-1
                )

                ),
                go.Scatter(
                x0=0,
                dx=1,
                y= y_waarden,
                name=' ='+str(afgelegde_weg)+'m',
                mode='none',
                fill='tozeroy',
                fillcolor='rgba(0,102,204,.3)',
                line=dict(
                shape='spline',
                smoothing=1.3,
                simplify=False
                )

                ),
                go.Scatter(
                x=[max(0,len(y_waarden)-20),max(0,len(y_waarden)-20)],
                y=[0.9*min(laatstegetallen),1.1*max(laatstegetallen)],
                mode='lines',
                visible=True,
                showlegend=False,
                line=dict(
                color='rgba(0,0,0,1)',
                dash='solid',
                width=2
                )
                ),
                go.Scatter(
                x= [max(0,len(y_waarden)-20),max(25,len(y_waarden)+5)],
                y= [0.9*min(laatstegetallen),0.9*min(laatstegetallen)],
                mode='lines',
                visible=True,
                showlegend=False,
                line=dict(
                color='rgba(0,0,0,1)',
                dash='solid',
                width=2
                )
                ) # voor meerdere grafieken op één plot, voeg hierna nog een commando toe vb. go.scatter. Pas wel op met instellingen, nu wordt steeds de oppervlakte onder grafiek gekleurd...
                ]

                , cls= plotly.utils.PlotlyJSONEncoder),
                'layout': json.dumps(go.Layout(
                showlegend=True,
                autosize=False,
                separators=',',
                paper_bgcolor='rgb(255,255,255,1)',
                plot_bgcolor='rgb(255,255,255,1)',
                hovermode='closest',

                title=dict(
                text='V[t]'
                ),

                legend=dict(
                orientation='v',
                itemsizing='constant',
                itemclick='toggle',
                itemdoubleclick='toggleothers',

                title=dict(
                text='legende:',
                side='top'
                )
                ),

                margin=dict(
                l=50,
                r=110,
                t=50,
                b=50,
                autoexpand=False
                ),

                modebar=dict(
                orientation='h',
                bgcolor='rgba(255,255,255,1)',
                color='rgba(128,128,128,1)',
                activecolor='rgba(0,0,128,1)'
                ),

                xaxis=dict(
                type='linear',
                range=[max(0,len(y_waarden)-20),max(25,len(y_waarden)+5)],


                title=dict(
                text='tijd in seconden'
                )
                ),

                yaxis=dict(
                type='linear',
                range=[0.9*min(laatstegetallen),1.1*max(laatstegetallen)],

                title=dict(
                text='snelheid in m/s'
                )
                )

                )
                , cls= plotly.utils.PlotlyJSONEncoder)
                }



                yield 'data:{0}\n\n'.format(json.dumps(grafiek))
        return Response(events_grafiek(),mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
