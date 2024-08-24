<!-- frontend/src/routes/service/+page.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';

	const API_URL = import.meta.env.VITE_API_URL;

	let isOpen = writable(false);
	function toggleMenu() {
		isOpen.update((n) => !n);
	}
	function handleEventCodeChange(event) {
		const selectedValue = event.target.value;

		if (selectedValue === 'eventCode1') {
			eventCode = 'PF343804';
		} else if (selectedValue === 'eventCode2') {
			eventCode = 'SomeEventCode2';
		} else if (selectedValue === 'eventCode3') {
			eventCode = 'SomeEventCode3';
		}
	}
	// 입력 필드와 연동될 변수들을 선언
	let eventCode = ''; // 공연코드
	let eventDate = ''; // 공연일시
	let discountAmount = ''; // 할인금액
	let pricePerTicket = ''; // 장당금액
	let gender = {
		maleCount: 0,
		femaleCount: 0,
		otherCount: 0
	}; // 성별
	let age = ''; // 연령
	// 추론된 취소수 값을 저장할 스토어
	let predictedCancellationCount = writable<number | null>(null);
	let flaskMessage: string = ''; // Flask로부터의 메시지 (오류 시 표시)
	let message: string = '';

	let predictedCount: number | null;
	$: predictedCount = $predictedCancellationCount;

	let eventImages = {
		PF343804: `${API_URL.replace('/api', '')}/static/images/PF343804.jpeg`,
		SomeEventCode2: `${API_URL.replace('/api', '')}/static/images/SomeImage2.jpeg`,
		SomeEventCode3: `${API_URL.replace('/api', '')}/static/images/SomeImage3.jpeg`
	};

	// let eventImages = {
	// 	PF343804: `https://yesshow.vercel.app/static/images/PF343804.jpeg`,
	// 	SomeEventCode2: `https://yesshow.vercel.app/static/images/PF343804.jpeg`,
	// 	SomeEventCode3: `https://yesshow.vercel.app/static/images/PF343804.jpeg`
	// };

	let selectedImageUrl: string | null = null;

	$: selectedImageUrl = eventCode ? eventImages[eventCode] : null;
	console.log('Selected image URL:', selectedImageUrl);

	// Flask 백엔드에서 메시지 가져오기
	onMount(async () => {
		try {
			const flaskResponse = await fetch(`${API_URL}/message`);
			// const flaskResponse = await fetch(`https://yesshow.vercel.app/api/message`);
			if (flaskResponse.ok) {
				const data = await flaskResponse.json();
				flaskMessage = data.message;
			} else {
				flaskMessage = 'Failed to load message';
			}
		} catch (error) {
			flaskMessage = 'Error: ' + error.message;
		}
	});

	// 취소수 예측 요청을 보내는 비동기 함수
	async function predictCancellation() {
		// 입력된 데이터를 객체로 묶음
		const data = {
			eventCode,
			eventDate,
			discountAmount,
			pricePerTicket,
			gender,
			age
		};

		console.log('Sending JSON data:', data); // JSON 데이터 출력

		try {
			// Flask 백엔드로 POST 요청을 보냄
			// const response = await fetch(`https://yesshow.vercel.app/api/predict`, {
			// 	method: 'POST',
			// 	headers: {
			// 		'Content-Type': 'application/json'
			// 	},
			// 	body: JSON.stringify(data) // 데이터를 JSON 형식으로 변환하여 전송
			// });
			const response = await fetch(`${API_URL}/predict`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data) // 데이터를 JSON 형식으로 변환하여 전송
			});

			if (response.ok) {
				// 성공 시, 예측 결과를 JSON으로 받아와 스토어에 저장
				const result = await response.json();
				predictedCancellationCount.set(result.predictedCancellationCount);
			} else {
				// 요청 실패 시 메시지 업데이트
				flaskMessage = 'Failed to load prediction';
			}
		} catch (error) {
			// 네트워크 또는 기타 오류 처리
			flaskMessage = 'Error: ' + error.message;
		}
	}
</script>

<main class="w-full max-w-[850px] mx-auto p-4 relative">
	<h1 class="text-2xl font-bold mb-4">Cancel Tickets Prediction</h1>

	<div class="mt-8">
		<h2 class="text-l font-semibold mb-2">공연코드 선택</h2>
		<div class="flex items-center gap-4">
			<div
				class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
			>
				<select
					id="eventCode"
					bind:value={eventCode}
					on:change={handleEventCodeChange}
					class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
					style="font-family: 'Noto Sans KR', sans-serif;"
					required
				>
					<option value="" disabled selected>공연코드 선택</option>
					<option value="PF343804">PF343804</option>
					<option value="SomeEventCode2"> - </option>
					<option value="SomeEventCode3"> - </option>
				</select>
			</div>
			{#if selectedImageUrl}
				<img
					src={selectedImageUrl}
					alt="Event Image"
					class="w-20 h-20 object-cover rounded-lg border border-gray-300"
				/>
			{/if}
		</div>
	</div>
	<br />

	<!-- 입력 폼 -->
	<form on:submit|preventDefault={predictCancellation}>
		<div class="grid grid-cols-2 gap-4">
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					공연코드
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="text"
						id="eventCode"
						bind:value={eventCode}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="공연코드"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					공연일시
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="datetime-local"
						id="eventDate"
						bind:value={eventDate}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					평균 할인금액
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="number"
						id="discountAmount"
						bind:value={discountAmount}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="평균 할인금액"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					평균 장당금액
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="number"
						id="pricePerTicket"
						bind:value={pricePerTicket}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="평균 장당금액"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
			<!-- 남자 인원 입력 필드 -->
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					남자 인원
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="number"
						id="maleCount"
						bind:value={gender.maleCount}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="남자 인원"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>

			<!-- 여자 인원 입력 필드 -->
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					여자 인원
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="number"
						id="femaleCount"
						bind:value={gender.femaleCount}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="여자 인원"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
			<!-- 기타 인원 입력 필드 추가 -->
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					기타 인원
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="number"
						id="otherCount"
						bind:value={gender.otherCount}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="기타 인원"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
			<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
				<div
					class="text-[#121212]/90 text-sm font-semibold tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					연령 평균
				</div>
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<input
						type="number"
						id="age"
						bind:value={age}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						placeholder="연령 평균"
						required
						style="font-family: 'Noto Sans KR', sans-serif;"
					/>
				</div>
			</div>
		</div>
		<div class="h-[120px] flex-col justify-center items-center gap-4 inline-flex mt-4">
			<div
				class="self-stretch h-14 p-3 bg-[#050a11] rounded-lg justify-center items-center gap-2 inline-flex"
			>
				<button
					type="submit"
					class="text-white text-lg font-semibold font-['Poppins'] tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif;"
				>
					예측하기
				</button>
			</div>
		</div>
	</form>

	<!-- 예측 결과를 표시하는 부분 -->
	<div class="mt-8">
		<h2 class="text-xl font-semibold mb-2">취소표 예측결과</h2>
		<p class="text-lg text-gray-700">
			{#if predictedCount !== null}
				{predictedCount}
			{:else}
				-
			{/if}
		</p>
	</div>
</main>
