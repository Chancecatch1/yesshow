<!-- frontend/src/lib/CancellationGraph.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';

	export let data = [];
	export let timePoints = {};

	let graphContainer;
	let containerHeight;
	let tooltip;
	let svg;
	let width;
	let height;
	let x;
	let y;

	onMount(() => {
		containerHeight = Math.min(500, window.innerHeight * 0.6);

		const margin = { top: 40, right: 30, bottom: 50, left: 60 };
		const containerWidth = graphContainer.clientWidth;
		width = containerWidth - margin.left - margin.right;
		height = containerHeight - margin.top - margin.bottom;

		svg = d3
			.select(graphContainer)
			.append('svg')
			.attr('width', '100%')
			.attr('height', containerHeight)
			.attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
			.append('g')
			.attr('transform', `translate(${margin.left},${margin.top})`);

		// Add a subtle background
		svg.append('rect').attr('width', width).attr('height', height).attr('fill', '#f0f0f0');

		x = d3
			.scaleLinear()
			.domain([0, d3.max(data, (d) => d.time)])
			.range([0, width]);

		y = d3.scaleLinear().domain([0, 1]).range([height, 0]);

		// Add grid lines
		svg
			.append('g')
			.attr('class', 'grid')
			.attr('transform', `translate(0,${height})`)
			.call(d3.axisBottom(x).tickSize(-height).tickFormat(''));

		svg.append('g').attr('class', 'grid').call(d3.axisLeft(y).tickSize(-width).tickFormat(''));

		// Style grid lines
		svg.selectAll('.grid line').style('stroke', '#e0e0e0').style('stroke-opacity', 0.7);
		svg.selectAll('.grid path').style('stroke-width', 0);

		// X-axis with label
		svg.append('g').attr('transform', `translate(0,${height})`).call(d3.axisBottom(x).ticks(10));

		svg
			.append('text')
			.attr('transform', `translate(${width / 2},${height + 33})`)
			.style('text-anchor', 'middle')
			.style('font-size', '0.8em')
			.text('시간 (Hour)');

		// Y-axis with label
		svg.append('g').call(d3.axisLeft(y).tickFormat(d3.format('.0%')));

		svg
			.append('text')
			.attr('transform', 'rotate(-90)')
			.attr('y', 0 - margin.left)
			.attr('x', 0 - height / 2)
			.attr('dy', '1.5em')
			.style('text-anchor', 'middle')
			.style('font-size', '0.8em')
			.text('취소 확률');

		// Create a gradient for the line
		const gradient = svg
			.append('defs')
			.append('linearGradient')
			.attr('id', 'line-gradient')
			.attr('gradientUnits', 'userSpaceOnUse')
			.attr('x1', 0)
			.attr('y1', y(0))
			.attr('x2', 0)
			.attr('y2', y(1));

		gradient.append('stop').attr('offset', '0%').attr('stop-color', '#4a90e2');
		gradient.append('stop').attr('offset', '100%').attr('stop-color', '#7b3ff2');

		// Draw the line
		const line = d3
			.line()
			.x((d) => x(d.time))
			.y((d) => y(d.probability))
			.curve(d3.curveMonotoneX);

		svg
			.append('path')
			.datum(data)
			.attr('fill', 'none')
			.attr('stroke', 'url(#line-gradient)')
			.attr('stroke-width', 3)
			.attr('d', line);

		// Create tooltip
		tooltip = d3
			.select(graphContainer)
			.append('div')
			.attr('class', 'tooltip')
			.style('opacity', 0)
			.style('position', 'absolute')
			.attr(
				'class',
				'bg-white text-black border border-gray-300 rounded p-2 shadow-lg pointer-events-none'
			);

		// Add mouse events and tooltip functionality
		addMouseInteractions();

		// Add time lines
		addTimeLine(timePoints.t20, '#ff6b6b', '20%');
		addTimeLine(timePoints.t50, '#4ecdc4', '50%');
		addTimeLine(timePoints.t90, '#45b7d1', '90%');

		// Add title
		svg
			.append('text')
			.attr('x', width / 2)
			.attr('y', -margin.top / 2)
			.attr('text-anchor', 'middle')
			.style('font-size', '16px')
			.style('font-weight', 'bold')
			.text('시점별 취소확률');
	});

	function addMouseInteractions() {
		const mouseG = svg.append('g').attr('class', 'mouse-over-effects');

		const mouseLine = mouseG
			.append('path')
			.attr('class', 'mouse-line')
			.style('stroke', 'black')
			.style('stroke-width', '1px')
			.style('opacity', '0');

		const mousePerLine = mouseG.append('g').attr('class', 'mouse-per-line');

		const mouseCircle = mousePerLine
			.append('circle')
			.attr('r', 7)
			.style('stroke', '#4a90e2')
			.style('fill', 'none')
			.style('stroke-width', '2px')
			.style('opacity', '0');

		mouseG
			.append('svg:rect')
			.attr('width', width)
			.attr('height', height)
			.attr('fill', 'none')
			.attr('pointer-events', 'all')
			.on('mouseout', function () {
				hideTooltip();
			})
			.on('mouseover', function () {
				showTooltip();
			})
			.on('mousemove', function (event) {
				const [mouseX, mouseY] = d3.pointer(event);
				updateTooltipPosition(mouseX, mouseY);
			});
	}

	function hideTooltip() {
		d3.select('.mouse-line').style('opacity', '0');
		d3.select('.mouse-per-line circle').style('opacity', '0');
		tooltip.style('opacity', 0);
	}

	function showTooltip() {
		d3.select('.mouse-line').style('opacity', '1');
		d3.select('.mouse-per-line circle').style('opacity', '1');
	}

	function updateTooltipPosition(mouseX, mouseY) {
		d3.select('.mouse-line').attr('d', `M${mouseX},${height} ${mouseX},0`).style('opacity', '1');

		const x0 = x.invert(mouseX);
		const bisect = d3.bisector((d) => d.time).left;
		const i = bisect(data, x0, 1);
		const d0 = data[i - 1];
		const d1 = data[i];
		const d = x0 - d0.time > d1.time - x0 ? d1 : d0;

		d3.select('.mouse-per-line circle')
			.attr('transform', `translate(${x(d.time)},${y(d.probability)})`)
			.style('opacity', '1');

		const tooltipWidth = 120;
		const tooltipHeight = 40;
		let tooltipLeft = mouseX + 60; // Adjusting for the margin.left
		let tooltipTop = mouseY + 40 - tooltipHeight; // Adjusting for the margin.top

		if (tooltipLeft + tooltipWidth > width) {
			tooltipLeft = mouseX + 60 - tooltipWidth;
		}

		if (tooltipTop < 0) {
			tooltipTop = mouseY + 40;
		}

		tooltip
			.style('opacity', 0.9)
			.html(`${(d.probability * 100).toFixed(2)}% at ${d.time.toFixed(2)} 시간`)
			.style('left', `${tooltipLeft}px`)
			.style('top', `${tooltipTop}px`);
	}

	function addTimeLine(time, color, label) {
		svg
			.append('line')
			.attr('x1', x(time))
			.attr('x2', x(time))
			.attr('y1', 0)
			.attr('y2', height)
			.attr('stroke', color)
			.style('stroke-dasharray', '3, 3');

		svg
			.append('text')
			.attr('x', x(time))
			.attr('y', -5)
			.attr('text-anchor', 'middle')
			.attr('fill', color)
			.style('font-size', '12px')
			.text(label);

		const timeLineTooltip = d3
			.select(graphContainer)
			.append('div')
			.attr('class', 'timeline-tooltip')
			.style('opacity', 0)
			.style('position', 'absolute')
			.attr(
				'class',
				'bg-white text-black border border-gray-300 rounded p-2 shadow-lg pointer-events-none'
			);

		svg
			.append('rect')
			.attr('x', x(time) - 5)
			.attr('y', 0)
			.attr('width', 10)
			.attr('height', height)
			.attr('fill', 'transparent')
			.on('mouseover', (event) => {
				const [mouseX, mouseY] = d3.pointer(event);
				timeLineTooltip
					.style('opacity', 0.9)
					.html(`${label} at ${time.toFixed(2)} 시간`)
					.style('left', `${mouseX + 60}px`)
					.style('top', `${mouseY + 40}px`);
			})
			.on('mouseout', () => {
				timeLineTooltip.style('opacity', 0);
			});
	}
</script>

<div
	bind:this={graphContainer}
	class="w-full h-[400px] mx-auto text-center bg-white shadow-lg rounded-lg p-4 relative"
	role="img"
	aria-label="시점별 취소확률 그래프"
	style="height: {containerHeight}px;"
></div>
