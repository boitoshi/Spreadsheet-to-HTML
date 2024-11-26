// DOMが読み込まれた後に実行される処理をまとめる
$(document).ready(function() {
    const elements = {
        form: $('#trainer_form'),
        sheetSelect: $('#sheet_name'),
        trainerSelect: $('#trainer_name'),
        generateBtn: $('#generate-btn'),
        result: $('#result'),
        resultContent: $('#result-content'),
        codeBlock: $('#code-block'),
        feedback: $('#feedback'),
        // spinner: $('#generate-btn .spinner-border'),
        copyBtn: $('#copy-btn')
    };

    elements.sheetSelect.change(loadTrainers); // シート名変更時にトレーナー一覧を取得
    elements.copyBtn.on('click', copyCode); // コピーボタンのイベントリスナー追加
    // elements.form.on('submit', handleFormSubmit);

    // 初期表示時にトレーナー一覧を取得
    loadTrainers();

    // シート名が変更されたときにトレーナー名を取得する関数
    function loadTrainers() {
        const sheetName = elements.sheetSelect.val();
        if (!sheetName) {
            showFeedback('地方を選ぶんじゃ🗺️', 'info');
            return;
        }

        // デバッグ用ログ
        console.log('Requesting trainers for sheet:', sheetName);

        // `/get_trainers`エンドポイントにAJAXリクエストを送信
        $.ajax({
            type: 'POST',
            url: '/get_trainers',
            data: { sheet_name: sheetName },
            success: function(trainers) {
                console.log('Received trainers:', trainers);  // デバッグ用ログ
            
                elements.trainerSelect.empty();
                if (Array.isArray(trainers)) {
                    trainers.forEach(function(trainer) {
                        elements.trainerSelect.append(new Option(trainer, trainer));
                    });
                } else if (trainers.error) {
                    showFeedback(trainers.error, 'danger');
                }
            },
            error: function(xhr, status, error) {
                console.error('API Error:', {
                    status: xhr.status,
                    statusText: xhr.statusText,
                    error: error
                });
                showFeedback('エラーが発生しました: ' + error, 'danger');
            }
        });
    }
    
    // クリーンアップ処理を追加
    $(window).on('unload', function() {
        // イベントリスナーの解除
        elements.sheetSelect.off('change');
        elements.form.off('submit');
        // AJAXリクエストが進行中の場合は中止
        $.active && $.ajax().abort();
    });

    // フォーム送信時の処理
    elements.form.on('submit', async function(event) {
        event.preventDefault();
        try {
            elements.generateBtn.prop('disabled', true);
            
            const response = await $.ajax({
                type: 'POST',
                url: '/generate_html',
                data: $(this).serialize()
            });
            
            if (response.html_output) {
                elements.resultContent.html(response.html_output);
                elements.codeBlock.text(response.html_output);
                showFeedback('HTMLの生成に成功しました！', 'success');
            }
        } catch (error) {
            console.error('HTML生成エラー:', error);
            showFeedback('エラーが発生しました: ' + error, 'danger');
        } finally {
            elements.generateBtn.prop('disabled', false);
        }
    });

    // コピーボタンの処理
    async function copyCode() {
        const codeBlock = elements.codeBlock[0];  // DOM要素を取得
        const copyBtn = elements.copyBtn[0];      // DOM要素を取得
        // const codeBlock = document.getElementById('code-block');
        // const copyBtn = document.getElementById('copy-btn');


        if (!codeBlock || !codeBlock.textContent.trim()) {
            showFeedback('あれ？コピーする内容がないみたい...🤔', 'info');
            return;
        }
    
        try {
            // ボタンを一時的に無効化
            copyBtn.disabled = true;
            
            // innerTextを使用してHTMLの整形を維持
            await navigator.clipboard.writeText(codeBlock.innerText);
            // ボタンのアイコンとテキストを変更
            const buttonIcon = copyBtn.querySelector('i');
            buttonIcon.classList.remove('bi-clipboard');
            buttonIcon.classList.add('bi-clipboard-check-fill');
            
            showFeedback('コピーできたよ！✨', 'success');

            // 1秒後にアイコンを元に戻す
            setTimeout(() => {
                buttonIcon.classList.remove('bi-clipboard-check-fill');
                buttonIcon.classList.add('bi-clipboard');
            }, 1000);

        } catch (err) {
            console.error('Copy failed:', err);
            showFeedback('ごめんね！コピーできなかったみたい...😢', 'danger');
        } finally {
        // ボタンを再度有効化
            setTimeout(() => {
                copyBtn.disabled = false;
            }, 700);
        }    
    }
    
    // フィードバック表示関数
    function showFeedback(message, type) {
        const toastId = 'toast-' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast pop-toast text-bg-${type}" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body text-center w-100">
                        ${message}
                    </div>
                    <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="閉じる"></button>
                </div>
            </div>
        `;
    
        // トーストコンテナのスタイルを変更
        const $toastContainer = $('#toast-container');
    
        $toastContainer.append(toastHtml);
    
        // const toastElement = document.getElementById(toastId);
        // const toast = new bootstrap.Toast(toastElement, { 
        //     autohide: true,
        //     delay: 1500
        // });
        // toast.show();
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 1500
        });
        toast.show();

        // 非表示後に要素を削除
        $(`#${toastId}`).on('hidden.bs.toast', function() {
            $(this).remove();
        // toastElement.addEventListener('hidden.bs.toast', function () {
        //     toastElement.remove();
        });
    };
});
