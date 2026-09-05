/**
 * TÂM GIAO (SoulEcho) - Core Client Script
 * Hỗ trợ kết nối REST API FastAPI (khi server chạy) và Fallback thông minh chạy độc lập trên trình duyệt.
 */

const API_BASE_URL = "http://127.0.0.1:8000/api";

// Trạng thái người dùng hiện tại
let currentUser = {
  id: 99,
  username: "user_test",
  displayName: "Bạn",
  isAnonymous: true,
  alias: "Mầm Nhỏ #204",
  avatar: "🌱",
  survey: {
    ageBracket: "18-22",
    lifeStage: "Sinh viên",
    primaryIssues: ["Áp lực học tập", "Cô đơn / Khó hòa nhập"],
    goals: ["Tìm một người biết lắng nghe", "Tìm bạn cùng học"],
    preferredFormat: "both",
    storySummary: "Mình là sinh viên năm nhất đang cảm thấy rất bỡ ngỡ và áp lực trước kỳ thi sắp tới.",
    urgencyLevel: 2
  }
};

// Dữ liệu mẫu người dùng ứng viên
let candidateUsers = [
  {
    userId: 1,
    displayName: "Minh Anh",
    anonymousAlias: "Mầm Nhỏ #142",
    isAnonymous: true,
    avatar: "🌱",
    ageBracket: "18 - 22 tuổi",
    lifeStage: "Sinh viên năm nhất",
    primaryIssues: ["Áp lực học tập", "Cô đơn", "Tự ti năng lực"],
    storySummary: "Môi trường đại học quá khác biệt làm mình thường xuyên tự ti và thấy bản thân tụt lại phía sau so với bạn bè.",
    similarityScore: 92,
    matchReasons: "Cùng là sinh viên năm nhất · Cùng trăn trở về Áp lực học tập · Đều mong tìm người lắng nghe",
    urgencyLevel: 2
  },
  {
    userId: 2,
    displayName: "Hoàng Long",
    anonymousAlias: "Đom Đóm #89",
    isAnonymous: true,
    avatar: "✨",
    ageBracket: "23 - 27 tuổi",
    lifeStage: "Mới đi làm",
    primaryIssues: ["Burnout công việc", "Áp lực gia đình", "Lo âu tương lai"],
    storySummary: "Đi làm công sở 1 năm nhưng ngày nào cũng thấy kiệt sức, bố mẹ ở quê luôn kỳ vọng mình phải thành đạt gửi tiền về.",
    similarityScore: 81,
    matchReasons: "Cùng chịu áp lực kỳ vọng · Mong muốn giải tỏa gánh nặng tâm lý",
    urgencyLevel: 2
  },
  {
    userId: 3,
    displayName: "Bảo Ngọc",
    anonymousAlias: "Mây Trắng #215",
    isAnonymous: true,
    avatar: "🕊️",
    ageBracket: "18 - 22 tuổi",
    lifeStage: "Sinh viên năm 3",
    primaryIssues: ["Đổ vỡ tình cảm", "Overthinking", "Cô đơn"],
    storySummary: "Vừa chia tay mối tình 3 năm, cảm giác trống rỗng và mất đi một phần cuộc sống. Muốn tìm bạn tâm sự để vượt qua giai đoạn này.",
    similarityScore: 78,
    matchReasons: "Cùng độ tuổi 18-22 · Cùng cảm giác cô đơn và overthinking",
    urgencyLevel: 3
  },
  {
    userId: 4,
    displayName: "Đình Phong",
    anonymousAlias: "Gió Mùa #304",
    isAnonymous: true,
    avatar: "🍂",
    ageBracket: "15 - 18 tuổi",
    lifeStage: "Học sinh THPT",
    primaryIssues: ["Áp lực thi cử", "Mâu thuẫn gia đình", "Tự ti"],
    storySummary: "Lớp 12 áp lực thi đại học nặng nề, gia đình luôn so sánh với con nhà người ta khiến mình không dám về nhà.",
    similarityScore: 84,
    matchReasons: "Cùng gặp áp lực thi cử và học đường · Mong tìm người bạn đồng cảm",
    urgencyLevel: 2
  },
  {
    userId: 5,
    displayName: "Phương Thảo",
    anonymousAlias: "Hướng Dương #77",
    isAnonymous: true,
    avatar: "🌻",
    ageBracket: "18 - 22 tuổi",
    lifeStage: "Sinh viên năm 3 (Đã từng vượt qua)",
    primaryIssues: ["Áp lực học tập", "Phát triển bản thân"],
    storySummary: "Năm nhất mình từng nợ môn và khóc rất nhiều, nhưng giờ mình đã vượt qua. Mình ở đây để lắng nghe và chia sẻ kinh nghiệm.",
    similarityScore: 89,
    matchReasons: "Người đi trước có kinh nghiệm · Sẵn sàng đồng hành cùng tân sinh viên",
    urgencyLevel: 1
  }
];

// Dữ liệu mẫu nhóm gợi ý
let candidateGroups = [
  {
    id: 1,
    name: "Trạm Trú Ẩn: Áp Lực Học Tập Năm Nhất",
    description: "Nhóm nhỏ 2–5 bạn sinh viên năm nhất cùng giãi bày về cảm giác chới với trước giảng đường, thi cử và cách thích nghi.",
    category: "Áp lực học tập",
    isMicroGroup: true,
    maxMembers: 5,
    currentMembers: 3,
    icon: "🌱",
    matchPercentage: 96,
    matchReasons: "Nhóm nhỏ 2–5 người · Đúng chủ đề áp lực học tập và sinh viên năm nhất",
    tags: ["Áp lực học tập", "Sinh viên", "Cô đơn"]
  },
  {
    id: 2,
    name: "Vòng Tròn Lắng Nghe: Kỳ Vọng Gia Đình",
    description: "Nơi những người con chịu gánh nặng 'con nhà người ta' cùng ngồi lại, không phán xét, trao nhau cái ôm ấm áp.",
    category: "Gia đình",
    isMicroGroup: true,
    maxMembers: 5,
    currentMembers: 2,
    icon: "🕯️",
    matchPercentage: 86,
    matchReasons: "Nhóm nhỏ an toàn · Chữa lành tổn thương kỳ vọng gia đình",
    tags: ["Mâu thuẫn gia đình", "Tự ti"]
  },
  {
    id: 3,
    name: "Chữa Lành Sau Đổ Vỡ Tình Cảm",
    description: "Vòng tròn 2–5 người cùng sẻ chia câu chuyện tan vỡ, khích lệ nhau tập trung yêu lấy chính mình.",
    category: "Tình cảm",
    isMicroGroup: true,
    maxMembers: 5,
    currentMembers: 4,
    icon: "🕊️",
    matchPercentage: 75,
    matchReasons: "Nhóm nhỏ kín đáo · Tìm lại bình yên sau tổn thương tình cảm",
    tags: ["Đổ vỡ tình cảm", "Chữa lành"]
  },
  {
    id: 4,
    name: "Sinh Viên & Khủng Hoảng Tuổi 20",
    description: "Cộng đồng chia sẻ các băn khoăn về định hướng nghề nghiệp, kỹ năng sống và cách duy trì sức khỏe tinh thần.",
    category: "Phát triển bản thân",
    isMicroGroup: false,
    maxMembers: 200,
    currentMembers: 142,
    icon: "🎓",
    matchPercentage: 90,
    matchReasons: "Cộng đồng sinh viên rộng mở · Nhiều góc nhìn tích cực",
    tags: ["Sinh viên", "Phát triển bản thân"]
  },
  {
    id: 5,
    name: "Xả Căng Thẳng Sau Giờ Làm & Burnout",
    description: "Dành cho các bạn trẻ mới đi làm đối mặt với deadline, sếp khó tính và mong muốn tìm lại sự cân bằng.",
    category: "Burnout công việc",
    isMicroGroup: false,
    maxMembers: 150,
    currentMembers: 88,
    icon: "💼",
    matchPercentage: 80,
    matchReasons: "Cân bằng cuộc sống & chữa lành căng thẳng công việc",
    tags: ["Burnout công việc", "Mới đi làm"]
  }
];

// Dữ liệu chuyên gia
let expertList = [
  {
    id: 1,
    name: "ThS. Lê Hoàng Yến",
    title: "Thạc sĩ Tâm lý Lâm sàng",
    specialty: "Tham vấn học đường & Khủng hoảng thanh thiếu niên",
    bio: "8 năm công tác tại Phòng Tham vấn Tâm lý Học đường. Đồng hành cùng hơn 1.200 học sinh, sinh viên vượt qua áp lực thi cử và trầm cảm nhẹ.",
    rating: 4.9,
    experience: "8 năm kinh nghiệm",
    time: "Thứ 2, 4, 6 (18:30 - 21:00)",
    avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80",
    org: "Trung tâm Tham vấn Tâm lý Sư Phạm"
  },
  {
    id: 2,
    name: "TS. Nguyễn Minh Triết",
    title: "Tiến sĩ Tâm lý học - Trị liệu Gia đình",
    specialty: "Hàn gắn mâu thuẫn phụ huynh & Khủng hoảng tuổi trưởng thành",
    bio: "Tốt nghiệp ĐH Paris 8, chuyên sâu về giải tỏa căng thẳng gia đình, xóa bỏ khoảng cách thế hệ và giúp người trẻ tìm lại kết nối với cha mẹ.",
    rating: 5.0,
    experience: "12 năm kinh nghiệm",
    time: "Thứ 3, 5, 7 (19:00 - 21:30)",
    avatar: "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=150&auto=format&fit=crop&q=80",
    org: "Viện Sức khỏe Tinh thần & Hành vi"
  },
  {
    id: 3,
    name: "ThS. Đỗ Thu Trang",
    title: "Chuyên gia Hướng nghiệp & Sức khỏe Tinh thần",
    specialty: "Burnout công sở, Rối loạn lo âu xã hội (Imposter Syndrome)",
    bio: "Hỗ trợ người mới ra trường vượt qua cảm giác hoang mang, tự ti năng lực và xây dựng ranh giới lành mạnh trong môi trường công việc.",
    rating: 4.8,
    experience: "6 năm kinh nghiệm",
    time: "Thứ 7, CN (09:00 - 16:00)",
    avatar: "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&auto=format&fit=crop&q=80",
    org: "Mạng lưới Career & Mental Health VN"
  }
];

// Lịch sử tin nhắn của các phòng chat
let chatConversations = {
  1: [
    { sender: "partner", name: "Mầm Nhỏ #142", text: "Chào bạn, mình thấy hệ thống ghép hai đứa mình vì cùng là sinh viên năm nhất đang chịu áp lực học tập...", time: "10:15" },
    { sender: "me", name: "Bạn", text: "Chào bạn nhé! Đúng rồi, đợt này trường mình thi liên miên, nhiều đêm mình mất ngủ vì sợ nợ môn.", time: "10:17" },
    { sender: "partner", name: "Mầm Nhỏ #142", text: "Mình cũng y hệt luôn 😢 Nhiều lúc thấy bạn bè xung quanh ai cũng giỏi giang, mình cứ có cảm giác mình là người kém cỏi nhất lớp.", time: "10:18" }
  ],
  2: [
    { sender: "partner", name: "Đom Đóm #89", text: "Chào bạn, hôm nay công việc của bạn có quá tải không?", time: "Hôm qua" }
  ],
  101: [
    { sender: "partner", name: "Điều Phối Viên Tâm Giao", text: "Chào mừng các bạn đến với Trạm Trú Ẩn #1 (Áp lực học tập năm nhất). Phòng chat này có tối đa 5 thành viên, mọi chia sẻ đều được giữ kín và tôn trọng tuyệt đối.", time: "Hôm qua" },
    { sender: "partner", name: "Mầm Nhỏ #142", text: "Chào cả nhà ạ, em là sinh viên năm nhất Bách Khoa.", time: "09:30" }
  ]
};

let currentActiveChatId = 1;

// ================= KHỞI TẠO ỨNG DỤNG =================
document.addEventListener("DOMContentLoaded", () => {
  renderUserRecommendations(candidateUsers);
  renderGroupRecommendations(candidateGroups);
  renderExperts(expertList);
  renderChatRoomList();
  renderChatMessages(currentActiveChatId);
  renderJournalHistory();
  tryFetchBackendData();
});

// Thử gọi FastAPI backend nếu đang chạy
async function tryFetchBackendData() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`, { signal: AbortSignal.timeout(1500) });
    if (res.ok) {
      console.log("✅ Đã kết nối thành công với Backend FastAPI (http://localhost:8000)");
      // Nạp danh sách từ backend
      const usersRes = await fetch(`${API_BASE_URL}/recommendations/users/${currentUser.id}`);
      if (usersRes.ok) {
        const data = await usersRes.json();
        if (data && data.length > 0) {
          candidateUsers = data;
          renderUserRecommendations(candidateUsers);
        }
      }
    }
  } catch (err) {
    console.log("ℹ️ Đang chạy ở chế độ Client-Side thông minh (Không cần backend vẫn hoạt động 100%)");
  }
}

// ================= ĐIỀU HƯỚNG TABS/VIEWS =================
function switchView(viewName) {
  const views = ["discover", "groups", "chat", "wellness", "experts"];
  views.forEach(v => {
    const el = document.getElementById(`view-${v}`);
    const tab = document.getElementById(`tab-${v}`);
    if (el) el.style.display = (v === viewName) ? "block" : "none";
    if (tab) tab.classList.toggle("active", v === viewName);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ================= HIỂN THỊ ĐỀ XUẤT NGƯỜI DÙNG 1-1 =================
function renderUserRecommendations(users) {
  const container = document.getElementById("userRecommendationsGrid");
  if (!container) return;

  container.innerHTML = users.map(u => `
    <div class="user-card">
      <div>
        <div class="card-top">
          <div class="user-header-info">
            <div class="user-avatar-large">${u.avatar || "🌱"}</div>
            <div>
              <strong style="font-size: 1.05rem;">${u.isAnonymous ? u.anonymousAlias : u.displayName}</strong>
              <div style="font-size: 0.8rem; color: var(--text-muted);">${u.ageBracket} · ${u.lifeStage}</div>
            </div>
          </div>
          <div class="similarity-badge">
            ⚡ ${u.similarityScore}% tương đồng
          </div>
        </div>

        <div class="card-reason">
          💡 ${u.matchReasons}
        </div>

        <div class="card-story">
          "${u.storySummary}"
        </div>

        <div class="card-tags">
          ${(u.primaryIssues || []).map(t => `<span class="tag-badge">#${t}</span>`).join("")}
        </div>
      </div>

      <div class="card-actions">
        <button class="btn-secondary" onclick="openAnonymousChatWith(${u.userId || u.id}, '${u.isAnonymous ? u.anonymousAlias : u.displayName}')">
          💬 Nhắn Tin Ẩn Danh
        </button>
        <button class="btn-primary" onclick="startVoiceCallWith('${u.isAnonymous ? u.anonymousAlias : u.displayName}')">
          📞 Gọi Thoại
        </button>
      </div>
    </div>
  `).join("");
}

// ================= HIỂN THỊ ĐỀ XUẤT NHÓM =================
function renderGroupRecommendations(groups) {
  const container = document.getElementById("groupRecommendationsGrid");
  if (!container) return;

  container.innerHTML = groups.map(g => `
    <div class="group-card">
      <div>
        <div class="card-top">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div class="user-avatar-large" style="background: var(--primary-light);">${g.icon}</div>
            <div>
              <strong style="font-size: 1.05rem;">${g.name}</strong>
              <div style="font-size: 0.8rem; color: var(--text-muted);">
                ${g.isMicroGroup ? "🔒 Vòng tròn nhỏ 2–5 người" : "🌐 Cộng đồng mở"} · ${g.currentMembers}/${g.maxMembers} thành viên
              </div>
            </div>
          </div>
          <div class="similarity-badge" style="background: #f1effd; color: #6c5ce7; border-color: rgba(108, 92, 231, 0.2);">
            🎯 ${g.matchPercentage}% phù hợp
          </div>
        </div>

        <div class="card-reason" style="border-left-color: #6c5ce7; color: #5243c2;">
          💡 ${g.matchReasons}
        </div>

        <p style="font-size: 0.92rem; color: var(--text-main); margin-bottom: 1rem; line-height: 1.5;">
          ${g.description}
        </p>

        <div class="card-tags">
          ${(g.tags || []).map(t => `<span class="tag-badge">#${t}</span>`).join("")}
        </div>
      </div>

      <div class="card-actions">
        <button class="btn-primary" onclick="joinGroupChat(${g.id}, '${g.name}')">
          🚪 Tham Gia Trò Chuyện
        </button>
      </div>
    </div>
  `).join("");
}

// ================= BỘ LỌC ĐỀ XUẤT =================
function filterDiscover(category, btn) {
  document.querySelectorAll("#view-discover .pill-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");

  if (category === "all") {
    renderUserRecommendations(candidateUsers);
  } else {
    const filtered = candidateUsers.filter(u => 
      u.primaryIssues.some(i => i.toLowerCase().includes(category.toLowerCase()))
    );
    renderUserRecommendations(filtered.length ? filtered : candidateUsers);
  }
}

function filterGroups(type, btn) {
  document.querySelectorAll("#view-groups .pill-btn").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");

  if (type === "all") {
    renderGroupRecommendations(candidateGroups);
  } else if (type === "micro") {
    renderGroupRecommendations(candidateGroups.filter(g => g.isMicroGroup));
  } else {
    renderGroupRecommendations(candidateGroups.filter(g => !g.isMicroGroup));
  }
}

// ================= PHÒNG TRÒ CHUYỆN & TIN NHẮN =================
function renderChatRoomList() {
  const listEl = document.getElementById("chatRoomList");
  if (!listEl) return;

  const rooms = [
    { id: 1, name: "Mầm Nhỏ #142", avatar: "🌱", sub: "92% tương đồng · Sinh viên năm nhất" },
    { id: 2, name: "Đom Đóm #89", avatar: "✨", sub: "81% tương đồng · Burnout công việc" },
    { id: 101, name: "Trạm Trú Ẩn #1 (Áp lực học tập)", avatar: "🏫", sub: "Nhóm 3/5 bạn cùng hoàn cảnh" }
  ];

  listEl.innerHTML = rooms.map(r => `
    <li class="chat-room-item ${r.id === currentActiveChatId ? 'active' : ''}" onclick="selectChatRoom(${r.id}, '${r.name}', '${r.avatar}', '${r.sub}')">
      <div class="user-avatar-mini">${r.avatar}</div>
      <div style="overflow: hidden;">
        <strong style="font-size: 0.9rem; display: block; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">${r.name}</strong>
        <span style="font-size: 0.75rem; color: var(--text-muted);">${r.sub}</span>
      </div>
    </li>
  `).join("");
}

function selectChatRoom(id, name, avatar, sub) {
  currentActiveChatId = id;
  renderChatRoomList();
  
  document.getElementById("currentChatName").innerText = name;
  document.getElementById("currentChatAvatar").innerText = avatar;
  document.getElementById("currentChatSub").innerText = sub;

  renderChatMessages(id);
}

function renderChatMessages(roomId) {
  const container = document.getElementById("chatMessagesContainer");
  if (!container) return;

  const messages = chatConversations[roomId] || [];
  container.innerHTML = messages.map(m => `
    <div class="msg-bubble ${m.sender === 'me' ? 'me' : 'partner'} ${m.isCrisis ? 'crisis-alert' : ''}">
      <div class="msg-sender-name">${m.name} · ${m.time}</div>
      <div>${m.text}</div>
    </div>
  `).join("");

  container.scrollTop = container.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("chatInput");
  const text = input.value.trim();
  if (!text) return;

  // Kiểm tra từ khóa nhạy cảm / tự hại
  const crisisKeywords = ["tự tử", "tự hại", "chết đi", "không muốn sống", "kết thúc tất cả"];
  const hasCrisis = crisisKeywords.some(kw => text.toLowerCase().includes(kw));

  if (!chatConversations[currentActiveChatId]) {
    chatConversations[currentActiveChatId] = [];
  }

  const now = new Date();
  const timeStr = `${now.getHours()}:${now.getMinutes() < 10 ? '0' : ''}${now.getMinutes()}`;

  // Thêm tin nhắn của người dùng
  chatConversations[currentActiveChatId].push({
    sender: "me",
    name: currentUser.isAnonymous ? currentUser.alias : currentUser.displayName,
    text: text,
    time: timeStr
  });

  input.value = "";
  renderChatMessages(currentActiveChatId);

  // Nếu có từ khóa khủng hoảng -> Cảnh báo SOS ngay
  if (hasCrisis) {
    setTimeout(() => {
      chatConversations[currentActiveChatId].push({
        sender: "partner",
        name: "Hệ Thống An Toàn Tâm Giao",
        text: "🚨 Chúng mình cảm nhận bạn đang trải qua sự tổn thương hoặc áp lực vô cùng nặng nề. Xin đừng chịu đựng một mình! Hãy bấm nút 'Cứu Trợ SOS' ở góc trên để liên hệ ngay Hotline Ngày Mai (096 306 1414) hoặc Tổng đài 111 hoàn toàn miễn phí.",
        time: timeStr,
        isCrisis: true
      });
      renderChatMessages(currentActiveChatId);
      openSOSModal();
    }, 500);
    return;
  }

  // Giả lập phản hồi thấu cảm tự động từ người bạn
  setTimeout(() => {
    const sampleResponses = [
      "Mình hiểu cảm giác này của bạn. Cảm ơn bạn đã tin tưởng chia sẻ với mình nhé! ❤️",
      "Thật sự rất mệt mỏi đúng không? Mình cũng từng có những ngày chỉ muốn trốn khỏi tất cả.",
      "Bạn đã rất cố gắng rồi. Cứ chậm lại một chút nhé, không cần phải gồng mình mãi đâu.",
      "Mình ở đây lắng nghe bạn, bạn cứ nói hết ra cho nhẹ lòng nhé! 🤗"
    ];
    const reply = sampleResponses[Math.floor(Math.random() * sampleResponses.length)];
    
    chatConversations[currentActiveChatId].push({
      sender: "partner",
      name: document.getElementById("currentChatName").innerText.split("(")[0].trim(),
      text: reply,
      time: timeStr
    });
    renderChatMessages(currentActiveChatId);
  }, 1400);
}

function handleChatEnter(e) {
  if (e.key === "Enter") sendMessage();
}

function sendIcebreaker(promptText) {
  const input = document.getElementById("chatInput");
  input.value = promptText;
  sendMessage();
}

function sendReaction(reaction) {
  const input = document.getElementById("chatInput");
  input.value = `[Gửi ${reaction}]`;
  sendMessage();
}

function openAnonymousChatWith(userId, name) {
  currentActiveChatId = userId;
  switchView("chat");
  selectChatRoom(userId, name, "🌱", "92% tương đồng · Đang trực tuyến");
}

function joinGroupChat(groupId, groupName) {
  currentActiveChatId = 100 + groupId;
  switchView("chat");
  selectChatRoom(currentActiveChatId, groupName, "👥", "Nhóm cùng hoàn cảnh");
}

function reportUser() {
  alert("Cảm ơn bạn. Báo cáo đã được gửi tới Ban Điều Phối Tâm Giao. Chúng mình sẽ kiểm duyệt tin nhắn trong phòng để đảm bảo an toàn tuyệt đối cho bạn.");
}

// ================= CUỘC GỌI THOẠI ẨN DANH (VOICE CALL) =================
let callInterval = null;
let callSeconds = 0;

function startVoiceCallWith(name) {
  document.getElementById("voicePartnerName").innerText = name;
  openVoiceCallModal();
}

function openVoiceCallModal() {
  document.getElementById("voiceCallModal").classList.add("active");
  callSeconds = 0;
  callInterval = setInterval(() => {
    callSeconds++;
    const mins = Math.floor(callSeconds / 60);
    const secs = callSeconds % 60;
    document.getElementById("voiceCallTimer").innerText = 
      `${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
  }, 1000);
}

function closeVoiceCallModal() {
  document.getElementById("voiceCallModal").classList.remove("active");
  if (callInterval) clearInterval(callInterval);
}

function endVoiceCall() {
  closeVoiceCallModal();
  alert("Cuộc gọi ẩn danh đã kết thúc an toàn. Không có bất kỳ thông tin cá nhân nào bị lưu trữ.");
}

function toggleMuteCall(btn) {
  if (btn.innerText === "🎙️") {
    btn.innerText = "🔇";
    btn.title = "Đã tắt Micro";
  } else {
    btn.innerText = "🎙️";
    btn.title = "Đã bật Micro";
  }
}

// ================= BÀI TẬP THỞ 4-7-8 =================
let isBreathing = false;
let breathTimeout = null;

function startQuickBreathing() {
  switchView("wellness");
  setTimeout(() => {
    toggleBreathingExercise();
  }, 300);
}

function toggleBreathingExercise() {
  const btn = document.getElementById("btnToggleBreath");
  const circle = document.getElementById("breathingCircle");
  const countEl = document.getElementById("breathingCount");
  const statusEl = document.getElementById("breathingStatus");

  if (isBreathing) {
    // Dừng bài tập
    isBreathing = false;
    clearTimeout(breathTimeout);
    circle.className = "breathing-circle";
    countEl.innerText = "Bắt đầu";
    statusEl.innerText = "Đã dừng bài tập thở";
    btn.innerText = "Bắt Đầu Bài Tập Thở";
    return;
  }

  isBreathing = true;
  btn.innerText = "Dừng Bài Tập Thở";
  runBreathingCycle(circle, countEl, statusEl);
}

function runBreathingCycle(circle, countEl, statusEl) {
  if (!isBreathing) return;

  // Giai đoạn 1: HÍT VÀO (4 giây)
  circle.className = "breathing-circle inhale";
  statusEl.innerText = "Hít vào từ từ bằng mũi...";
  let c = 4;
  countEl.innerText = c;
  
  const timerInhale = setInterval(() => {
    c--;
    if (c > 0) countEl.innerText = c;
    else clearInterval(timerInhale);
  }, 1000);

  breathTimeout = setTimeout(() => {
    if (!isBreathing) return;
    
    // Giai đoạn 2: GIỮ HƠI (7 giây)
    circle.className = "breathing-circle hold";
    statusEl.innerText = "Giữ hơi thở nhẹ nhàng trong lồng ngực...";
    let h = 7;
    countEl.innerText = h;
    const timerHold = setInterval(() => {
      h--;
      if (h > 0) countEl.innerText = h;
      else clearInterval(timerHold);
    }, 1000);

    breathTimeout = setTimeout(() => {
      if (!isBreathing) return;

      // Giai đoạn 3: THỞ RA (8 giây)
      circle.className = "breathing-circle exhale";
      statusEl.innerText = "Thở ra chậm rãi qua miệng...";
      let e = 8;
      countEl.innerText = e;
      const timerExhale = setInterval(() => {
        e--;
        if (e > 0) countEl.innerText = e;
        else clearInterval(timerExhale);
      }, 1000);

      breathTimeout = setTimeout(() => {
        // Lặp lại chu kỳ tiếp theo
        runBreathingCycle(circle, countEl, statusEl);
      }, 8000);

    }, 7000);

  }, 4000);
}

// ================= TIẾP ĐẤT 5-4-3-2-1 (GROUNDING) =================
const groundingSteps = [
  { step: 1, title: "Bước 1: 5 đồ vật bạn có thể NHÌN THẤY", desc: "Hãy đưa mắt nhìn xung quanh và gọi tên 5 đồ vật (ví dụ: chiếc quạt, chiếc cốc, màn hình máy tính, bàn tay, ô cửa sổ...)." },
  { step: 2, title: "Bước 2: 4 bề mặt bạn có thể CHẠM VÀO", desc: "Chạm tay vào mặt bàn, vuốt nhẹ áo quần bạn đang mặc, cảm nhận lòng bàn chân chạm sàn nhà, chạm vào mặt kính điện thoại." },
  { step: 3, title: "Bước 3: 3 âm thanh bạn có thể NGHE THẤY", desc: "Lắng tai nghe tiếng quạt gió kêu, tiếng xe cộ phía xa, hay chính tiếng nhịp thở của bạn lúc này." },
  { step: 4, title: "Bước 4: 2 mùi hương bạn có thể NGỬI THẤY", desc: "Mùi sách vở, hương thơm thoang thoảng của căn phòng hoặc hít hà mùi chiếc áo sạch bạn đang mặc." },
  { step: 5, title: "Bước 5: 1 vị giác bạn cảm nhận được", desc: "Uống một ngụm nước mát và cảm nhận dòng nước lành chảy vào cơ thể. Bạn đang ở đây, an toàn và vững chãi." }
];
let currentGroundingIndex = 0;

function nextGroundingStep() {
  currentGroundingIndex = (currentGroundingIndex + 1) % groundingSteps.length;
  updateGroundingUI();
}

function prevGroundingStep() {
  currentGroundingIndex = (currentGroundingIndex - 1 + groundingSteps.length) % groundingSteps.length;
  updateGroundingUI();
}

function updateGroundingUI() {
  const item = groundingSteps[currentGroundingIndex];
  document.getElementById("groundingTitle").innerText = item.title;
  document.getElementById("groundingDesc").innerText = item.desc;
}

// ================= HỘP THƯ TỰ HỦY (BURN NOTE) =================
function burnNote() {
  const textarea = document.getElementById("burnInput");
  const text = textarea.value.trim();
  if (!text) {
    alert("Hãy viết vài dòng những uất ức hoặc áp lực bạn muốn trút bỏ trước nhé!");
    return;
  }

  textarea.classList.add("burning");
  setTimeout(() => {
    textarea.value = "";
    textarea.classList.remove("burning");
    alert("✨ Nỗi buồn và uất ức đã được hóa giải. Tâm hồn bạn xứng đáng được bình yên.");
  }, 1600);
}

// ================= SỔ TAY CẢM XÚC (JOURNALING) =================
let selectedMoodScore = 3;
let journalList = JSON.parse(localStorage.getItem("tamgiao_journals") || "[]");

function selectMood(score, btn) {
  selectedMoodScore = score;
  document.querySelectorAll("#moodSelector .btn-secondary").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
}

function saveJournalEntry() {
  const title = document.getElementById("journalTitle").value.trim();
  const content = document.getElementById("journalContent").value.trim();
  if (!content) {
    alert("Vui lòng nhập đôi dòng tâm sự để lưu vào sổ tay nhé.");
    return;
  }

  const moodLabels = ["", "😭 Rất tệ", "😔 Lo âu", "😐 Bình thường", "😊 Ổn định", "🥰 Rất tốt"];
  const newEntry = {
    id: Date.now(),
    mood: moodLabels[selectedMoodScore],
    title: title || "Ghi chép cảm xúc",
    content: content,
    date: new Date().toLocaleDateString("vi-VN", { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
  };

  journalList.unshift(newEntry);
  localStorage.setItem("tamgiao_journals", JSON.stringify(journalList));

  document.getElementById("journalTitle").value = "";
  document.getElementById("journalContent").value = "";
  renderJournalHistory();
  alert("Đã lưu trang nhật ký cảm xúc an toàn vào thiết bị của bạn!");
}

function renderJournalHistory() {
  const container = document.getElementById("journalEntriesList");
  if (!container) return;

  if (journalList.length === 0) {
    container.innerHTML = `<p style="font-size: 0.85rem; color: var(--text-muted); font-style: italic;">Chưa có trang nhật ký nào. Hãy viết đôi dòng cảm xúc của bạn hôm nay nhé.</p>`;
    return;
  }

  container.innerHTML = journalList.map(j => `
    <div style="background: #f8faf9; border: 1px solid var(--border-color); padding: 0.75rem; border-radius: 8px;">
      <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.2rem;">
        <span style="font-weight: 600; color: var(--primary);">${j.mood}</span>
        <span>${j.date}</span>
      </div>
      <strong style="font-size: 0.88rem; display: block; margin-bottom: 0.2rem;">${j.title}</strong>
      <p style="font-size: 0.84rem; color: var(--text-main); white-space: pre-wrap;">${j.content}</p>
    </div>
  `).join("");
}

// ================= CHUYÊN GIA & ĐẶT LỊCH =================
function renderExperts(experts) {
  const container = document.getElementById("expertsGrid");
  if (!container) return;

  container.innerHTML = experts.map(e => `
    <div class="user-card">
      <div>
        <div class="card-top">
          <div style="display: flex; gap: 0.75rem;">
            <img src="${e.avatar}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">
            <div>
              <strong style="font-size: 1.05rem;">${e.name}</strong>
              <div style="font-size: 0.8rem; color: var(--primary); font-weight: 600;">${e.title}</div>
              <div style="font-size: 0.76rem; color: var(--text-muted);">${e.org}</div>
            </div>
          </div>
          <div class="similarity-badge" style="background: #fff8e7; color: #d97706; border-color: #fde68a;">
            ⭐ ${e.rating} (${e.experience})
          </div>
        </div>

        <div style="font-size: 0.85rem; font-weight: 600; color: var(--text-main); margin-bottom: 0.4rem;">
          Chuyên môn: ${e.specialty}
        </div>

        <p style="font-size: 0.86rem; color: var(--text-muted); margin-bottom: 1rem; line-height: 1.45;">
          ${e.bio}
        </p>

        <div style="font-size: 0.8rem; background: #f8faf9; padding: 0.5rem; border-radius: 6px; margin-bottom: 1rem;">
          📅 Lịch rảnh: <strong>${e.time}</strong>
        </div>
      </div>

      <div class="card-actions">
        <button class="btn-primary" onclick="openBookExpertModal('${e.name}')">
          Đặt Lịch Tham Vấn
        </button>
      </div>
    </div>
  `).join("");
}

function openBookExpertModal(expertName) {
  document.getElementById("bookingExpertDesc").innerText = `Tham vấn bảo mật cùng ${expertName}`;
  document.getElementById("bookExpertModal").classList.add("active");
}

function closeBookExpertModal() {
  document.getElementById("bookExpertModal").classList.remove("active");
}

function confirmExpertBooking() {
  const time = document.getElementById("bookingTimeSelect").value;
  closeBookExpertModal();
  alert(`Yêu cầu tham vấn vào khung giờ "${time}" đã được ghi nhận! Phòng tham vấn sẽ liên hệ qua thông báo bảo mật trong vòng 24h.`);
}

function openPartnerRegisterModal() {
  document.getElementById("partnerModal").classList.add("active");
}

function closePartnerModal() {
  document.getElementById("partnerModal").classList.remove("active");
}

function submitPartnerRequest() {
  const org = document.getElementById("partnerOrgName").value.trim();
  if (!org) {
    alert("Vui lòng điền tên đơn vị trường học / tổ chức của bạn.");
    return;
  }
  closePartnerModal();
  alert("Cảm ơn đơn vị của bạn! Ban Phát Triển Mạng Lưới Học Đường Tâm Giao sẽ gửi hồ sơ đối tác trong 48h.");
}

// ================= MODAL KHẢO SÁT ĐA BƯỚC =================
let currentSurveyStep = 1;

function openSurveyModal() {
  currentSurveyStep = 1;
  updateSurveyStepUI();
  document.getElementById("surveyModal").classList.add("active");
}

function closeSurveyModal() {
  document.getElementById("surveyModal").classList.remove("active");
}

function nextSurveyStep(step) {
  currentSurveyStep = step;
  updateSurveyStepUI();
}

function prevSurveyStep(step) {
  currentSurveyStep = step;
  updateSurveyStepUI();
}

function updateSurveyStepUI() {
  for (let i = 1; i <= 4; i++) {
    const sstep = document.getElementById(`sstep-${i}`);
    const sbar = document.getElementById(`sbar-${i}`);
    if (sstep) sstep.classList.toggle("active", i === currentSurveyStep);
    if (sbar) sbar.classList.toggle("active", i <= currentSurveyStep);
  }
}

function selectSingleOpt(btn, groupType) {
  const parent = btn.parentElement;
  parent.querySelectorAll(".option-btn").forEach(b => b.classList.remove("selected"));
  btn.classList.add("selected");
}

function toggleMultiOpt(btn) {
  btn.classList.toggle("selected");
}

function generateNewAlias() {
  const adjs = ["Mầm", "Mây", "Đom Đóm", "Gió", "Cỏ May", "Sao Băng", "Ánh Nắng", "Biển Xanh", "Hạt Mưa"];
  const nouns = ["Nhỏ", "Trắng", "Hiền", "Thì Thầm", "Ấm Áp", "Lặng Lẽ", "Bình Yên", "Vươn Lên"];
  const randNum = Math.floor(Math.random() * 900) + 100;
  const newAlias = `${adjs[Math.floor(Math.random() * adjs.length)]} ${nouns[Math.floor(Math.random() * nouns.length)]} #${randNum}`;
  document.getElementById("aliasInput").value = newAlias;
}

function completeSurvey() {
  // Thu thập câu trả lời
  const selectedAge = document.querySelector("#optAge .option-btn.selected")?.innerText || "18-22";
  const selectedStage = document.querySelector("#optStage .option-btn.selected")?.innerText || "Sinh viên";
  
  const selectedIssues = [];
  document.querySelectorAll("#optIssues .option-btn.selected").forEach(b => {
    selectedIssues.push(b.innerText.replace(/^[^\s]+\s/, '')); // bỏ emoji đầu
  });

  const selectedGoals = [];
  document.querySelectorAll("#optGoals .option-btn.selected").forEach(b => {
    selectedGoals.push(b.innerText.replace(/^[^\s]+\s/, ''));
  });

  const story = document.getElementById("surveyStoryInput").value.trim();
  const alias = document.getElementById("aliasInput").value.trim() || "Mầm Nhỏ";

  currentUser.alias = alias;
  currentUser.survey = {
    ageBracket: selectedAge,
    lifeStage: selectedStage,
    primaryIssues: selectedIssues.length ? selectedIssues : ["Áp lực học tập"],
    goals: selectedGoals,
    storySummary: story,
    preferredFormat: "both"
  };

  // Cập nhật giao diện thanh điều hướng
  document.getElementById("navUserName").innerText = alias;
  document.getElementById("heroTitle").innerText = `Chào ${alias}, Trạm Lắng Nghe đã sẵn sàng vì bạn!`;
  document.getElementById("heroSubtitle").innerText = `Thuật toán đã phân tích hồ sơ: Bạn đang trăn trở về [${selectedIssues.join(", ")}]. Dưới đây là những người bạn và nhóm nhỏ đồng điệu nhất!`;

  closeSurveyModal();

  // Chạy thuật toán đo độ tương đồng trên Client
  recalculateMatchingScores(selectedIssues, selectedStage);

  alert(`🎉 Khảo sát hoàn tất! Thuật toán đã tối ưu danh sách ghép đôi theo chủ đề: ${selectedIssues.join(", ")}.`);
}

function recalculateMatchingScores(userIssues, userStage) {
  // Tính toán lại điểm số tương đồng cho candidateUsers
  candidateUsers.forEach(u => {
    let overlap = 0;
    userIssues.forEach(ui => {
      if (u.primaryIssues.some(pi => pi.toLowerCase().includes(ui.toLowerCase()) || ui.toLowerCase().includes(pi.toLowerCase()))) {
        overlap += 1;
      }
    });
    const stageMatch = u.lifeStage.toLowerCase().includes(userStage.toLowerCase()) ? 20 : 10;
    const newScore = Math.min(98, Math.max(62, 60 + (overlap * 12) + stageMatch));
    u.similarityScore = newScore;
  });

  candidateUsers.sort((a, b) => b.similarityScore - a.similarityScore);
  renderUserRecommendations(candidateUsers);

  // Tính toán lại cho nhóm
  candidateGroups.forEach(g => {
    let match = 0;
    userIssues.forEach(ui => {
      if (g.category.toLowerCase().includes(ui.toLowerCase()) || g.tags.some(t => t.toLowerCase().includes(ui.toLowerCase()))) {
        match += 15;
      }
    });
    g.matchPercentage = Math.min(98, Math.max(65, 68 + match));
  });
  candidateGroups.sort((a, b) => b.matchPercentage - a.matchPercentage);
  renderGroupRecommendations(candidateGroups);
}

// ================= CÁC MODAL KHÁC =================
function toggleAnonymousMode() {
  currentUser.isAnonymous = !currentUser.isAnonymous;
  const badgeName = document.getElementById("navUserName");
  const badgeMode = document.getElementById("navUserMode");

  if (currentUser.isAnonymous) {
    badgeName.innerText = currentUser.alias;
    badgeMode.innerText = "Chế độ Ẩn danh (Bảo mật)";
    badgeMode.style.color = "#2e7d5b";
  } else {
    badgeName.innerText = currentUser.displayName;
    badgeMode.innerText = "Chế độ Công khai";
    badgeMode.style.color = "#6c5ce7";
  }
}

function openSOSModal() {
  document.getElementById("sosModal").classList.add("active");
}

function closeSOSModal() {
  document.getElementById("sosModal").classList.remove("active");
}

function openConductModal(e) {
  if (e) e.preventDefault();
  document.getElementById("conductModal").classList.add("active");
}

function closeConductModal() {
  document.getElementById("conductModal").classList.remove("active");
}

