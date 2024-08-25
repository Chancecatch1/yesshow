<!-- frontend/src/lib/components/Header.svelte -->

<div class="w-full h-[78px] bg-white relative mb-14">
	<div class="absolute left-[10%] top-[30.5px] flex space-x-12">
		<div class="text-center text-[#1e1e1e] text-sm font-normal opacity-50 font-['Outfit']">
			<a href="/">Home</a>
			<!-- if hovering it, make underline -->
			<!-- <div class="w-full h-0 border-t-2 border-[#1e1e1e] mt-2"></div> -->
		</div>
		<div class="text-center text-[#1e1e1e] text-sm font-normal opacity-50 font-['Outfit']">
			<a href="/about">About</a>
		</div>
		<div class="text-center text-[#1e1e1e] text-sm font-normal opacity-50 font-['Outfit']">
			<a href="/insight">Insight</a>
		</div>
		<div class="text-center text-[#1e1e1e] text-sm font-normal opacity-50 font-['Outfit']">
			<a href="/service">Service</a>
		</div>
	</div>
	<div class="absolute left-1/2 transform -translate-x-1/2 top-[23px]">
		<div class="text-center text-[#1e1e1e] text-lg font-bold font-['Outfit']">YESSHOW</div>
	</div>
</div>
