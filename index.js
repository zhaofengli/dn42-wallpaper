const simulation = d3.forceSimulation();
const homeAs = '4242421926';

window.onload = () => {
  d3.json('data.json').then((data) => {
    console.log(data);
    const graph = d3.select('#graph');

    const peeringSel = graph
      .append('g')
      .selectAll('line')
      .data(data.peerings)
      .enter()
      .append('line');

    const asSel = graph
      .append('g')
      .selectAll('circle')
      .data(data.as)
      .enter()
      .append('circle')
      .attr('r', 8)
      .attr('fill', as => as.asn === homeAs ? 'red' : '#42A5F5');
      
    const updateLinks = () => {
      peeringSel
        .attr('x1', peering => peering.source.x)
        .attr('y1', peering => peering.source.y)
        .attr('x2', peering => peering.target.x)
        .attr('y2', peering => peering.target.y);

      asSel
        .attr('cx', as => as.x)
        .attr('cy', as => as.y);
    }
      
    simulation
      .force('link', d3.forceLink().id(as => as.asn))
      .force('center', d3.forceCenter(750, 500))
      .force('charge', d3.forceManyBody());
          
    simulation
      .nodes(data.as)
      .on('tick', updateLinks);
      
    simulation
      .force('link')
      .links(data.peerings);
      
    simulation
      .force('charge')
      .strength(-50);
  });
};
