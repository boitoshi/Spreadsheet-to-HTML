function toggleTrainerForm() {
// DOMが読み込まれた後に実行される処理をまとめる
$(document).ready(function() {
    const form = $('#trainer_form');
    const sheetSelect = $('#sheet_name');
    const trainerSelect = $('#trainer_name');
    const generateBtn = $('#generate-btn');
    const spinner = generateBtn.find('.spinner-border');
    const feedback = $('#feedback');

    // シート名が変更されたときにトレーナー名を取得する関数
    function loadTrainers() {
        var sheetName = sheetSelect.val();

        // `/get_trainers`エンドポイントにAJAXリクエストを送信
        $.ajax({
            type: 'POST',
            url: '/get_trainers',
            data: { sheet_name: sheetName },
            success: function(trainers) {
                var trainerSelect = $('#trainer_name');
                trainerSelect.empty();

                if (Array.isArray(trainers)) {
                    trainers.forEach(function(trainer) {
                        trainerSelect.append(new Option(trainer, trainer));
                    });
                } else if (trainers.error) {
                    alert('エラー: ' + trainers.error);
                }
            },
            error: function(xhr, status, error) {
                alert('エラーが発生しました: ' + error);
            }
        });
    }

    // フォーム送信時の処理
    form.submit(function(event) {
        event.preventDefault();

        // ローディング状態の表示
        generateBtn.prop('disabled', true);
        spinner.removeClass('d-none');
        feedback.addClass('d-none');

        $.ajax({
            type: 'POST',
            url: '/generate_html',
            data: $(this).serialize(),
            success: function(response) {
                if (response.html_output) {
                    $('#result').html(response.html_output);
                    $('#code-block').text(response.html_output);
                    showFeedback('HTMLの生成に成功しました！', 'success');
                } else if (response.error) {
                    showFeedback(response.error, 'danger');
                }
            },
            error: function(xhr, status, error) {
                showFeedback('エラーが発生しました: ' + error, 'danger');
            },
            complete: function() {
                generateBtn.prop('disabled', false);
                spinner.addClass('d-none');
            }
        });
    });

    // シート名変更時にトレーナー一覧を取得
    $('#sheet_name').change(loadTrainers);

    // 初期表示時にトレーナー一覧を取得
    loadTrainers();

    // コピーボタンの処理
    function copyCode() {
        const codeBlock = document.getElementById('code-block');
        if (codeBlock) {
            navigator.clipboard.writeText(codeBlock.innerText)
                .then(() => alert('HTMLコードをコピーしました！'))
                .catch((err) => console.error('コピーに失敗しました:', err));
        } else {
            console.error('code-block element not found');
        }
    }
    
    // フィードバック表示関数
    function showFeedback(message, type) {
        feedback
            .removeClass('d-none alert-success alert-danger')
            .addClass('alert-' + type)
            .text(message);
    }
});
}
