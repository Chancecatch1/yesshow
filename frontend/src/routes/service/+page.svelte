<!-- frontend/src/routes/service/+page.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { fade } from 'svelte/transition';

	const API_URL = import.meta.env.VITE_API_URL;

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

	let eventCode = '';
	let eventDate = '';
	let discountAmount = '';
	let pricePerTicket = '';
	let gender = {
		gender_1: 0,
		gender_2: 0,
		gender_0: 0
	};
	let age = '';
	let paymentDetails = {
		cardPayment: 0,
		otherPayment: 0,
		bankTransfer: 0,
		multiplePayments: 0,
		cashPayment: 0
	};
	let discountDetails = {
		otherDiscount: 0,
		selfDiscount: 0
	};

	let predictedCancellationCount = writable<number | null>(null);
	let flaskMessage: string = '';

	let predictedCount: number | null;
	$: predictedCount = $predictedCancellationCount;
	let predictedRemainingSeats: number | null = null;

	let eventImages = {
		PF343804: '/images/PF343804.jpeg',
		SomeEventCode2: '/images/PF343804.jpeg',
		SomeEventCode3: '/images/PF343804.jpeg'
	};

	let selectedImageUrl: string | null = null;
	$: selectedImageUrl = eventCode ? eventImages[eventCode] : null;

	onMount(async () => {
		try {
			const flaskResponse = await fetch(`${API_URL}/message`);
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

	async function predictCancellation() {
		const data = {
			eventCode,
			eventDate,
			discountAmount,
			pricePerTicket,
			gender,
			age,
			paymentDetails,
			discountDetails
		};

		try {
			const response = await fetch(`${API_URL}/predict`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			});

			if (response.ok) {
				const result = await response.json();
				predictedCancellationCount.set(result.predictedCancellationCount);
				predictedRemainingSeats = result.predictedRemainingSeats;
			} else {
				flaskMessage = 'Failed to load prediction';
			}
		} catch (error) {
			flaskMessage = 'Error: ' + error.message;
		}
	}

	function resetFields() {
		eventCode = '';
		eventDate = '';
		discountAmount = '';
		pricePerTicket = '';
		gender = {
			gender_1: 0,
			gender_2: 0,
			gender_0: 0
		};
		age = '';
		paymentDetails = {
			cardPayment: 0,
			otherPayment: 0,
			bankTransfer: 0,
			multiplePayments: 0,
			cashPayment: 0
		};
		discountDetails = {
			otherDiscount: 0,
			selfDiscount: 0
		};
		predictedCancellationCount.set(null);
		selectedImageUrl = null;
		predictedRemainingSeats = null;
	}
</script>

<main class="w-full max-w-[850px] mx-auto p-4 relative">
	<div class="relative">
		<h1 class="text-2xl font-bold mb-4">공연 취소 예측 서비스</h1>

		{#if selectedImageUrl}
			<div
				class="absolute top-0 left-[400px] w-32 h-32 z-10"
				in:fade={{ duration: 150, delay: 100 }}
				out:fade={{ duration: 150 }}
			>
				<img
					src={selectedImageUrl}
					alt="Event Image"
					class="w-full h-full object-cover rounded-lg border border-gray-300"
				/>
			</div>
		{/if}
	</div>

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
		</div>
	</div>
	<br />

	{#if eventCode}
		<form
			on:submit|preventDefault={predictCancellation}
			in:fade={{ duration: 200 }}
			out:fade={{ duration: 200 }}
		>
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
							step="0.01"
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
							step="0.01"
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
						gender_1 인원수
					</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="gender_1"
							bind:value={gender.gender_1}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="gender1 인원"
							step="0.01"
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
						gender_2 인원수
					</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="gender_2"
							bind:value={gender.gender_2}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="gender2 인원"
							step="0.01"
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
						gender_0 인원수
					</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="gender_0"
							bind:value={gender.gender_0}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="gender0 인원"
							step="0.01"
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
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">카드 결제 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="cardPayment"
							bind:value={paymentDetails.cardPayment}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="카드 결제 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">기타 결제 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="otherPayment"
							bind:value={paymentDetails.otherPayment}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="기타 결제 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">무통장 결제 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="bankTransfer"
							bind:value={paymentDetails.bankTransfer}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="무통장 결제 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">다중 결제 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="multiplePayments"
							bind:value={paymentDetails.multiplePayments}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="다중 결제 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">현금 결제 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="cashPayment"
							bind:value={paymentDetails.cashPayment}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="현금 결제 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">기타 할인 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="otherDiscount"
							bind:value={discountDetails.otherDiscount}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="기타 할인 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
				<div class="h-[77px] flex-col justify-start items-start gap-2 inline-flex">
					<div class="text-[#121212]/90 text-sm font-semibold tracking-wide">자체 할인 인원</div>
					<div
						class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
					>
						<input
							type="number"
							id="selfDiscount"
							bind:value={discountDetails.selfDiscount}
							class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
							placeholder="자체 할인 인원"
							step="0.01"
							required
							style="font-family: 'Noto Sans KR', sans-serif;"
						/>
					</div>
				</div>
			</div>
			<div class="h-[120px] flex justify-start items-center gap-4 mt-4">
				<div class="h-14 p-3 bg-[#050a11] rounded-lg flex justify-center items-center gap-2">
					<button
						type="submit"
						class="text-white text-sm font-semibold font-['Poppins'] tracking-wide"
						style="font-family: 'Noto Sans KR', sans-serif;"
					>
						예측하기
					</button>
				</div>
				<div class="h-14 p-3 bg-[#d1d5db] rounded-lg flex justify-center items-center gap-2">
					<button
						type="button"
						on:click={resetFields}
						class="text-black text-sm font-semibold font-['Poppins'] tracking-wide"
						style="font-family: 'Noto Sans KR', sans-serif;"
					>
						다시하기
					</button>
				</div>
			</div>

			<!-- 예측 결과 섹션들 -->
			<div class="mt-4">
				<div class="flex items-center gap-4">
					<div class="h-14 p-3 bg-white rounded-lg border border-gray-300 flex items-center">
						<h2 class="text-sm font-semibold">취소표 개수 예측</h2>
					</div>
					<div class="h-14 p-3 bg-white flex items-center">
						<p class="text-sm text-gray-700">
							{#if predictedCount !== null}
								{predictedCount}
							{:else}{/if}
						</p>
					</div>
				</div>
				<div class="flex items-center gap-4 mt-4">
					<div class="h-14 p-3 bg-white rounded-lg border border-gray-300 flex items-center">
						<h2 class="text-sm font-semibold">남은 좌석수 예측</h2>
					</div>
					<div class="h-14 p-3 bg-white flex items-center">
						<p class="text-sm text-gray-700">
							{#if predictedRemainingSeats !== null}
								{predictedRemainingSeats}
							{:else}{/if}
						</p>
					</div>
				</div>
			</div>
			<br />
			<div class="mt-8 text-center">
				{#if predictedRemainingSeats !== null}
					<div class="mt-8 text-center">
						{#if selectedImageUrl}
							<div class="h-auto inline-block">
								<img
									src="/images/pf343804_probability.png"
									alt="Probability Image"
									class="object-contain rounded-lg border border-gray-300"
								/>
							</div>
							<div
								class="text-[#121212]/90 text-l font-semibold tracking-wide mt-2"
								style="font-family: 'Noto Sans KR', sans-serif;"
							>
								시간에 따른 취소 확률
							</div>
						{/if}
					</div>
				{/if}
			</div>
		</form>
	{/if}
</main>
